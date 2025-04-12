<div align="center">
<p align="center">

<!-- prettier-ignore -->
<img src="https://cdn.prod.website-files.com/62cd5ce03261cba217188442/66dac501a8e9a90495970876_Logo%20dark-short-p-800.png" height="50px">

**The open-source tool curating datasets**

---

[![PyPI python](https://img.shields.io/pypi/pyversions/lightly-purple)](https://pypi.org/project/lightly-purple)
[![PyPI version](https://badge.fury.io/py/fiftyone.svg)](https://pypi.org/project/fiftyone)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

</p>
</div>

# 🚀 Aloha!

We at **[Lightly](https://lightly.ai)** created an open-source tool that supercharges your data curation workflows by enabling you to explore datasets, analyze data quality, and improve your machine learning pipelines more efficiently than ever before. Embark with us in this adventure of building better datasets.

## 💻 **Installation**

Please use Python 3.8 or higher with venv.

The library is not OS-dependent and should work on Windows, Linux, and macOS.

```shell
# Create a virtual environment
# On Linux/macOS:
python3 -m venv venv
source venv/bin/activate

# On Windows:
python -m venv venv
.\venv\Scripts\activate

# Install library
pip install lightly-purple

```

## **Quickstart**

Download the dataset and run a quickstart script to load your dataset and launch the app.

### **YOLO8 dataset example**

Here is a quick example using the YOLO8 dataset:

<details>
<summary>The YOLO format details:</summary>

```
dataset/
├── train/
│   ├── images/
│   │   ├── image1.jpg
│   │   ├── image2.jpg
│   │   └── ...
│   └── labels/
│       ├── image1.txt
│       ├── image2.txt
│       └── ...
├── valid/  (optional)
│   ├── images/
│   │   └── ...
│   └── labels/
│       └── ...
└── data.yaml
```

Each label file should contain YOLO format annotations (one per line):

```
<class> <x_center> <y_center> <width> <height>
```

Where coordinates are normalized between 0 and 1.

</details>

On Linux/MacOS:

```shell
# Download and extract dataset
export DATASET_PATH=$(pwd)/example-dataset && \
    bash <(curl -sL https://raw.githubusercontent.com/lightly-ai/gists/refs/heads/main/fetch-dataset.sh) \
 https://universe.roboflow.com/ds/nToYP9Q1ix\?key\=pnjUGTjjba \
        $DATASET_PATH

# Download example script
curl -sL https://raw.githubusercontent.com/lightly-ai/gists/refs/heads/main/example-yolo8.py > example.py

# Run the example script
python example.py
```

On Windows:

```shell
# Download and extract dataset
$DATASET_PATH = "$(Get-Location)\example-dataset"
[System.Environment]::SetEnvironmentVariable("DATASET_PATH", $DATASET_PATH, "Process")
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/lightly-ai/gists/refs/heads/main/fetch-dataset.ps1" -OutFile "fetch-dataset.ps1"
.\fetch-dataset.ps1 "https://universe.roboflow.com/ds/nToYP9Q1ix?key=pnjUGTjjba" "$DATASET_PATH"

# Download example script
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/lightly-ai/gists/refs/heads/main/example-yolo8.py" -OutFile "example.py"

# Run the example script
python.exe example.py
```

<details>
<summary>Quickstart commands explanation</summary>

1. **Setting up the dataset path**:

```shell
  export DATASET_PATH=$(pwd)/example-dataset
```

This creates an environment variable `DATASET_PATH` pointing to an 'example-dataset' folder in your current directory.

2. **Downloading and extracting the dataset**:

```shell
  bash <(curl -sL https://raw.githubusercontent.com/lightly-ai/gists/refs/heads/main/fetch-dataset.sh)
```

- Downloads a shell script that handles dataset fetching
- The script downloads a YOLO-format dataset from Roboflow
- Automatically extracts the dataset to your specified `DATASET_PATH`

3. **Getting the example code**:

```shell
  curl -sL https://raw.githubusercontent.com/lightly-ai/gists/refs/heads/main/example-yolo8.py > example.py
```

Downloads a Python script that demonstrates how to:

- Load the YOLO dataset
- Process the images and annotations
- Launch the Lightly Purple UI for exploration

4. **Running the example**:

```shell
  python example.py
```

Executes the downloaded script, which will:

- Initialize the dataset processor
- Load and analyze your data
- Start a local server
- Open the UI in your default web browser
</details>

## **Example explanation**

Let's break down the `example.py` script to explore the dataset:

```python
# We import the DatasetLoader class from the lightly_purple module
from lightly_purple import DatasetLoader

# Create a DatasetLoader instance
loader = DatasetLoader()

# We point to the yaml file describing the dataset
# and the input images subfolder.
# We use train subfolder.
loader.from_yolo(
    "dataset/data.yaml",
    "train",
)

# We start the UI application
loader.launch()

```

### **COCO dataset example**

Here is an example using the COCO dataset:

<details>
<summary>The COCO format details:</summary>

```
dataset/
├── train/                   # Image files used to train
│   ├── image1.jpg
│   ├── image2.jpg
│   └── ...
└── _annotations.coco.json        # Single JSON file containing all annotations
```

COCO uses a single JSON file containing all annotations. The format consists of three main components:

- Images: Defines metadata for each image in the dataset.
- Categories: Defines the object classes.
- Annotations: Defines object instances.

</details>

On Linux/MacOS:

```shell
# Download and extract dataset
export DATASET_PATH=$(pwd)/example-dataset/train && \
    bash <(curl -sL https://raw.githubusercontent.com/lightly-ai/gists/refs/heads/main/fetch-dataset.sh) \
 https://universe.roboflow.com/ds/XU8JobBB7x?key=rpuS7P1Du4 \
        $DATASET_PATH

# Download example script
curl -sL https://raw.githubusercontent.com/lightly-ai/gists/refs/heads/main/example-coco.py > example.py

# Run the example script
python example.py
```

On Windows:

```shell
# Download and extract dataset

Invoke-WebRequest -Uri "https://raw.githubusercontent.com/lightly-ai/gists/refs/heads/main/fetch-dataset.ps1" -OutFile "fetch-dataset.ps1"
.\fetch-dataset.ps1 "https://universe.roboflow.com/ds/XU8JobBB7x?key=rpuS7P1Du4" "$(Get-Location)\example-dataset"

# Download example script
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/lightly-ai/gists/refs/heads/main/example-coco.py" -OutFile "example.py"

$DATASET_PATH = "$(Get-Location)\example-dataset\train"
[System.Environment]::SetEnvironmentVariable("DATASET_PATH", $DATASET_PATH, "Process")
# Run the example script
python.exe example.py
```

## **Example explanation**

Let's break down the `example-coco.py` script to explore the dataset:

```python
from lightly_purple import DatasetLoader

# Create a DatasetLoader instance
loader = DatasetLoader()

# We point to the annotations json file and the input images folder.
# Defined dataset is processed here to be available for the UI application.
loader.from_coco_instance_segmentations(
    "dataset/_annotations.coco.json",
    "dataset/train",

# We start the UI application
loader.launch()

```

## 🔍 **How it works**

Let's describe a little bit in detail what is happening under the hood:

In our library, we emulated a full-fledged environment to process your data and make it available for the UI application.

- **Dataset Loader**: The Python module is responsible for processing the dataset.

  - Processes given dataset.
  - Stores it in the persistent data storage layer.
  - Handling various data formats and annotation types.

- **Data Storage Layer**: Stores information about the dataset:

  - After the dataset is processed information about the dataset is stored in the persistent database.
  - We use [duckdb database](https://duckdb.org/) as a persistent storage layer, you will see `purple.db` file after the dataset is processed.

- **Backend API**: Python web server that serves the dataset to the UI application.

  - Uses the persistent data storage layer to serve the dataset to the UI application.
  - Manages user interactions with the data

- **UI Application**: A responsive web interface:
  - Running on your local machine on 8001 port and available at http://localhost:8001/.
  - It opens automatically after the dataset is processed.
  - Consumes local API endpoints
  - Visualizes your dataset and analysis results

## 📦 **Dataset Formats**

Our library supports the following dataset formats:

- YOLO8
- COCO object detection
- COCO binary mask instance segmentation

## 📚 **FAQ**

### Are the datasets persistent?

Yes, the information about datasets is persistent and stored in the db file. You can see it after the dataset is processed.
If you rerun the loader it will create a new dataset representing the same dataset, keeping the previous dataset information untouched.

### Can I change the database path?

Not yet. The database is stored in the working directory by default.

### Can I launch in another Python script or do I have to do it in the same script?

It is possible to use only one script at the same time because we lock the db file for the duration of the script.

### Can I change the API backend port?

Currently, the API always runs on port 8001, and this cannot be changed yet.

### Can I process datasets that do not have annotations?

No, we support only datasets with annotations now.

### What dataset annotations are supported?

Bounding boxes are supported ✅

Instance segmentation is supported ✅

Custom metadata is NOT yet supported ❌
