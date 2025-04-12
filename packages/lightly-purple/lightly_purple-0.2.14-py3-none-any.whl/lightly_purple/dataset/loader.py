"""Dataset functionality module."""

from __future__ import annotations

import webbrowser
from pathlib import Path
from uuid import UUID

from labelformat.formats import (
    COCOInstanceSegmentationInput,
    COCOObjectDetectionInput,
    YOLOv8ObjectDetectionInput,
)
from labelformat.model.binary_mask_segmentation import BinaryMaskSegmentation
from labelformat.model.bounding_box import BoundingBoxFormat
from labelformat.model.image import Image
from labelformat.model.instance_segmentation import (
    ImageInstanceSegmentation,
    InstanceSegmentationInput,
)
from labelformat.model.multipolygon import MultiPolygon
from labelformat.model.object_detection import (
    ImageObjectDetection,
    ObjectDetectionInput,
)
from tqdm import tqdm

from lightly_purple.dataset.embedding_generator import (
    EmbeddingGenerator,
    RandomEmbeddingGenerator,
)
from lightly_purple.dataset.embedding_manager import EmbeddingManagerProvider
from lightly_purple.dataset.env import APP_URL, PURPLE_HOST, PURPLE_PORT
from lightly_purple.server.db import db_manager
from lightly_purple.server.models import Dataset, Sample
from lightly_purple.server.models.annotation import AnnotationInput
from lightly_purple.server.models.annotation_label import AnnotationLabelInput
from lightly_purple.server.models.dataset import DatasetInput
from lightly_purple.server.models.sample import SampleInput
from lightly_purple.server.models.tag import TagInput
from lightly_purple.server.resolvers.annotation import AnnotationResolver
from lightly_purple.server.resolvers.annotation_label import (
    AnnotationLabelResolver,
)
from lightly_purple.server.resolvers.dataset import DatasetResolver
from lightly_purple.server.resolvers.sample import SampleResolver
from lightly_purple.server.resolvers.tag import TagResolver
from lightly_purple.server.server import Server

# Constants
ANNOTATION_BATCH_SIZE = 64  # Number of annotations to process in a single batch
EMBEDDING_BATCH_SIZE = 64  # Number of embeddings to process in a single batch


class DatasetLoader:
    """Class responsible for loading datasets from various sources."""

    def __init__(self) -> None:
        """Initialize the dataset loader."""
        with db_manager.session() as session:
            self.dataset_resolver = DatasetResolver(session)
            self.tag_resolver = TagResolver(session)
            self.sample_resolver = SampleResolver(session)
            self.annotation_resolver = AnnotationResolver(session)
            self.embedding_manager = (
                EmbeddingManagerProvider.get_embedding_manager(session=session)
            )
            self.annotation_label_resolver = AnnotationLabelResolver(session)

    def _create_dataset(self, name: str, directory: str) -> Dataset:
        """Creates a new dataset."""
        with db_manager.session() as session:  # noqa: F841
            # Create dataset record
            dataset = DatasetInput(
                name=name,
                directory=directory,
            )
            return self.dataset_resolver.create(dataset)

    def _create_example_tags(self, dataset: Dataset) -> None:
        """Create example tags for samples and annotations."""
        self.tag_resolver.create(
            TagInput(
                dataset_id=dataset.dataset_id,
                name="label_mistakes",
                kind="sample",
            )
        )
        self.tag_resolver.create(
            TagInput(
                dataset_id=dataset.dataset_id,
                name="label_mistakes",
                kind="annotation",
            )
        )

    def _create_label_map(
        self, input_labels: ObjectDetectionInput | InstanceSegmentationInput
    ) -> dict[int, UUID]:
        """Create a mapping of category IDs to annotation label IDs."""
        label_map = {}
        for category in tqdm(
            input_labels.get_categories(),
            desc="Processing categories",
            unit=" categories",
        ):
            label = AnnotationLabelInput(annotation_label_name=category.name)
            stored_label = self.annotation_label_resolver.create(label)
            label_map[category.id] = stored_label.annotation_label_id
        return label_map

    def _process_object_detection_annotations(
        self,
        dataset: Dataset,
        image_data: ImageObjectDetection,
        stored_sample: Sample,
        label_map: dict[int, UUID],
        annotations_to_create: list[AnnotationInput],
    ) -> list[AnnotationInput]:
        """Process annotations for a single image."""
        for obj in image_data.objects:
            box = obj.box.to_format(BoundingBoxFormat.XYWH)
            x, y, width, height = box

            annotations_to_create.append(
                AnnotationInput(
                    dataset_id=dataset.dataset_id,
                    sample_id=stored_sample.sample_id,
                    annotation_label_id=label_map[obj.category.id],
                    x=x,
                    y=y,
                    width=width,
                    height=height,
                )
            )
        return annotations_to_create

    def _process_instance_segmentation_annotations(
        self,
        dataset: Dataset,
        image_data: ImageInstanceSegmentation,
        stored_sample: Sample,
        label_map: dict[int, UUID],
        annotations_to_create: list[AnnotationInput],
    ) -> list[AnnotationInput]:
        """Process annotations for a single image."""
        for obj in image_data.objects:
            segmentation_rle: None | list[int] = None
            if isinstance(obj.segmentation, MultiPolygon):
                box = obj.segmentation.bounding_box().to_format(
                    BoundingBoxFormat.XYWH
                )
            elif isinstance(obj.segmentation, BinaryMaskSegmentation):
                box = obj.segmentation.bounding_box.to_format(
                    BoundingBoxFormat.XYWH
                )
                segmentation_rle = obj.segmentation._rle_row_wise  # noqa: SLF001
            else:
                raise ValueError(
                    f"Unsupported segmentation type: {type(obj.segmentation)}"
                )

            x, y, width, height = box

            annotations_to_create.append(
                AnnotationInput(
                    dataset_id=dataset.dataset_id,
                    sample_id=stored_sample.sample_id,
                    annotation_label_id=label_map[obj.category.id],
                    x=x,
                    y=y,
                    width=width,
                    height=height,
                    segmentation__binary_mask__rle_row_wise=segmentation_rle,
                )
            )
        return annotations_to_create

    def _load_into_dataset(
        self,
        dataset: Dataset,
        input_labels: ObjectDetectionInput | InstanceSegmentationInput,
        img_dir: Path,
    ) -> None:
        """Store a loaded dataset in database."""
        # Create label mapping
        label_map = self._create_label_map(input_labels)

        # Create example tags.
        self._create_example_tags(dataset=dataset)

        annotations_to_create: list[AnnotationInput] = []
        sample_ids_for_embeddings = []

        # Load an embedding generator and register the model.
        embedding_generator = _load_embedding_generator()
        embedding_model = self.embedding_manager.register_embedding_model(
            dataset_id=dataset.dataset_id,
            embedding_generator=embedding_generator,
        )

        # Process images and annotations
        for image_data in tqdm(
            input_labels.get_labels(),
            desc="Processing images",
            unit=" images",
        ):
            # Mypy does not get that .image exists in both cases.
            image: Image = image_data.image  # type: ignore[attr-defined]
            # Create sample record
            sample = SampleInput(
                file_name=str(image.filename),
                file_path_abs=str(img_dir / image.filename),
                width=image.width,
                height=image.height,
                dataset_id=dataset.dataset_id,
            )
            stored_sample = self.sample_resolver.create(sample)
            sample_ids_for_embeddings.append(stored_sample.sample_id)
            # Process embedding batch if needed
            if len(sample_ids_for_embeddings) >= EMBEDDING_BATCH_SIZE:
                self.embedding_manager.embed_images(
                    sample_ids=sample_ids_for_embeddings,
                    embedding_model_id=embedding_model.embedding_model_id,
                )
                sample_ids_for_embeddings = []

            # Process annotations.
            if isinstance(image_data, ImageInstanceSegmentation):
                annotations_to_create = (
                    self._process_instance_segmentation_annotations(
                        dataset=dataset,
                        image_data=image_data,
                        stored_sample=stored_sample,
                        label_map=label_map,
                        annotations_to_create=annotations_to_create,
                    )
                )
            elif isinstance(image_data, ImageObjectDetection):
                annotations_to_create = (
                    self._process_object_detection_annotations(
                        dataset=dataset,
                        image_data=image_data,
                        stored_sample=stored_sample,
                        label_map=label_map,
                        annotations_to_create=annotations_to_create,
                    )
                )
            else:
                raise ValueError(
                    f"Unsupported annotation type: {type(image_data)}"
                )

            if len(annotations_to_create) >= ANNOTATION_BATCH_SIZE:
                self.annotation_resolver.create_many(annotations_to_create)
                annotations_to_create = []

        # Insert any remaining embeddings
        if sample_ids_for_embeddings:
            self.embedding_manager.embed_images(
                sample_ids=sample_ids_for_embeddings,
                embedding_model_id=embedding_model.embedding_model_id,
            )
            sample_ids_for_embeddings = []

        # Insert any remaining annotations
        if annotations_to_create:
            self.annotation_resolver.create_many(annotations_to_create)

    def from_yolo(
        self, data_yaml_path: str, input_split: str = "train"
    ) -> None:
        """Load a dataset in YOLO format and store in database."""
        data_yaml = Path(data_yaml_path)
        dataset = self._create_dataset(
            data_yaml.parent.name,
            str(data_yaml.parent.absolute()),
        )

        # Load the dataset
        label_input = YOLOv8ObjectDetectionInput(
            input_file=data_yaml,
            input_split=input_split,
        )
        # TODO(Kondrat 01/25): We need to expose images_dir from label_input
        img_dir = label_input._images_dir()  # noqa: SLF001
        self._load_into_dataset(dataset, label_input, img_dir)

    def from_coco_object_detections(
        self, annotations_json_path: str, input_images_folder: str
    ) -> None:
        """Load a dataset in COCO format and store in database."""
        annotations_json = Path(annotations_json_path)
        dataset = self._create_dataset(
            annotations_json.parent.name,
            str(annotations_json.parent.absolute()),
        )

        # Load the dataset
        label_input = COCOObjectDetectionInput(
            input_file=annotations_json,
        )
        img_dir = (
            Path(input_images_folder)
            if Path(input_images_folder).is_absolute()
            else annotations_json.parent / input_images_folder
        )
        self._load_into_dataset(dataset, label_input, img_dir)

    def from_coco_instance_segmentations(
        self, annotations_json_path: str, input_images_folder: str
    ) -> None:
        """Load a dataset in COCO format and store in database."""
        annotations_json = Path(annotations_json_path)
        dataset = self._create_dataset(
            annotations_json.parent.name,
            str(annotations_json.parent.absolute()),
        )

        # Load the dataset
        label_input = COCOInstanceSegmentationInput(
            input_file=annotations_json,
        )
        img_dir = (
            Path(input_images_folder)
            if Path(input_images_folder).is_absolute()
            else annotations_json.parent / input_images_folder
        )
        self._load_into_dataset(dataset, label_input, img_dir)

    def launch(self) -> None:
        """Launch the web interface for the loaded dataset."""
        server = Server(host=PURPLE_HOST, port=PURPLE_PORT)

        print(f"Opening URL: {APP_URL}")

        # We need to open browser before starting the server
        webbrowser.open_new(APP_URL)

        server.start()


def _load_embedding_generator() -> EmbeddingGenerator:
    """Load the embedding generator.

    Use MobileCLIP if its dependencies have been installed, otherwise use
    RandomEmbeddingGenerator.
    """
    try:
        from lightly_purple.dataset.mobileclip_embedding_generator import (
            MobileCLIPEmbeddingGenerator,
        )

        print("Using MobileCLIP embedding generator.")
        return MobileCLIPEmbeddingGenerator()
    except ImportError:
        print("Using random embedding generator.")
        return RandomEmbeddingGenerator()
