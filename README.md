![Thetis Logo](https://github.com/EFS-OpenSource/Thetis/blob/main/docs/source/_static/thetis-logo.png?raw=true)

--------------------------------------------------------------------------------

_Even if your AI is as strong as Achilles, Thetis will certainly know about its weaknesses._

Thetis is a service to examine safety-relevant aspects of AI algorithms (e.g., machine learning or deep learning models)
for uncertainty consistency (calibration), fairness, data quality, and robustness.

Please visit the [API Documentation Page](https://efs-opensource.github.io/Thetis/index.html) for the 
complete documentation and detailed backgrounds to the several safety aspects.

## Installation

Thetis is installed via the Python Package Index (PyPI) using Python's PIP-Tool. Simply type

```shell
$ pip install thetis
```

to install the latest version of Thetis for your Python environment.

## Obtain License

Request your **free evaluation license** at [efs-techhub.com](https://efs-techhub.com/efs-portfolio/loesungen/thetis).
Alternatively, use the included demo-licenses if you only wish to follow along with the [examples](examples).

Place the license file either in the working directory of your application or at:

* Windows: `<User>\\AppData\\Local\\Thetis\\license.dat`
* Unix: `~/.local/thetis/license.dat`

For further information about subscription models and license settings, see [Subscription](https://efs-opensource.github.io/Thetis/subscription.html).  
Your feedback is highly appreciated!

## Quickstart

### Classification Example

Thetis can evaluate the AI safety of classifier models.
In a first step, we demonstrate how to evaluate and rate your AI model using a basic classification
example from [scikit-learn](https://scikit-learn.org/).
The instructions below should be easy do adapt to your own use-case.

#### Example Data and Model Preparation

<details>
<summary>Click to show/hide example code for data and model preparation.</summary>

To start with our basic classification example, we need to load some data. In this tutorial, we use the
[Adult data set](https://www.openml.org/search?type=data&sort=runs&id=179&status=active).
This data set demonstrates a prediction task that determines whether a person earns over 50K a year.
Let us now load the data set using tools from the scikit-learn library.

*Note:* If your machine is behind a proxy server, downloading the example data as shown here may not work.
If that is the case for you, check out our detection example below.

```python
import pandas as pd
from sklearn.datasets import fetch_openml

testset_size = 10000

# use "fetch_openml" by scikit-learn to load "Adult" dataset from OpenML
dataset, target = fetch_openml(data_id=1590, return_X_y=True, parser="auto")

df_train, df_test = dataset.iloc[:-testset_size], dataset.iloc[-testset_size:]
target_train, target_test = target.iloc[:-testset_size], target.iloc[-testset_size:]

# drop columns with sensitive attributes from classifier input and convert categorical attributes to one-hot
df_train_cleared = df_train.drop(columns=["education", "race", "sex", "native-country", "relationship", "marital-status"])
df_test_cleared = df_test.drop(columns=["education", "race", "sex", "native-country", "relationship", "marital-status"])

# convert categorical columns to class codes with integer representation
categorical_columns = ["workclass", "occupation"]
df_train_cleared[categorical_columns] = df_train_cleared[categorical_columns].apply(lambda col: pd.Categorical(col).codes)
df_test_cleared[categorical_columns] = df_test_cleared[categorical_columns].apply(lambda col: pd.Categorical(col).codes)
```

This yields two [Pandas](https://pandas.pydata.org/) data frames with a reduced set of information.

In the next step, we train a simple Random Forest classifier on the training data using scikit-learn.
Furthermore, we make predictions on the test data using the trained model:

```python
from sklearn.ensemble import RandomForestClassifier

# initialize a Random Forest classifier and fit to training data
classifier = RandomForestClassifier(verbose=True)
classifier.fit(pd.get_dummies(df_train_cleared), target_train)

# finally, make predictions on the validation data set
confidence = classifier.predict_proba(pd.get_dummies(df_test_cleared))
labels = classifier.predict(pd.get_dummies(df_test_cleared))
```
</details>


#### Running AI Safety Evaluation with Thetis

For details of Thetis configuration, see section [Configuration](https://efs-opensource.github.io/Thetis/configuration.html). 
For the current example, you can download the [demo configuration file](https://raw.githubusercontent.com/EFS-OpenSource/Thetis/main/examples/demo_config_classification.yaml) 
from this repository or [click here](https://thetishostedfiles.blob.core.windows.net/demofiles/thetis_demo_classification.zip).

```python
from thetis import thetis

# use sensitive attributes during safety evaluation
annotations = pd.DataFrame({"target": target_test, "race": df_test["race"], "sex": df_test["sex"]})
predictions = pd.DataFrame({"labels": labels, "confidence": confidence[:, 1]}, index=annotations.index)

result = thetis(
    config="examples/demo_config_classification.yaml",
    annotations=annotations,
    predictions=predictions,
    output_dir="./output",
    license_file_path="examples/demo_license_classification.dat",
)
```

Thetis expects two Pandas data frames to run an evaluation:

* *Annotations*: `pd.DataFrame` with ground truth information about the data set. The column `target` is required, holding
  the ground truth target information. Furthermore, columns for sensitive attributes are expected that have been
  configured for the AI Fairness evaluation.
* *Predictions*: `pd.DataFrame` with the AI predictions for each sample in the data set. The columns `labels` and
  `confidence` are required, holding information about the predicted label and the respective prediction
  probability (model uncertainty or confidence).

Note that the indices of the data frames for annotations and predictions must match.

Thetis returns its findings, the final rating, and recommendations for mitigation strategies as a JSON-like dictionary.
We capture the dictionary as `result` and can access the different evaluation aspects:

* `result[<task>]['rating_score']` for the rating score of the selected task (e.g., 'fairness' or 'uncertainty').
* `result[<task>]['recommendations']` for the recommendations to mitigate possible issues of the selected task.
* `result[<task>]['rating_enum']` for a categorization of the actual aspect into `'GOOD'`, `'MEDIUM'`,
  or `'BAD'` depending on the rating score.


### Object Detection Example (Image-based)

Thetis is also capable of evaluating the AI safety of modern, image-based object detector models.
We utilize a [Faster R-CNN model by Torchvision](https://pytorch.org/vision/main/models/faster_rcnn.html) in conjunction
with a demo data set ([Download here](https://efs-techhub.com/efs-portfolio/loesungen/thetis)) to demonstrate the evaluation process for
object detectors. The instructions below should be easy do adapt to your own use-case.


#### Running Inference with PyTorch Object Detector

<details>
<summary>Click to show/hide example code for data and model preparation.</summary>

First, we need to load and initialize the [Faster R-CNN by Torchvision](https://pytorch.org/vision/main/models/faster_rcnn.html).

*Note:* If your machine is behind a proxy, you likely need to configure your environment so that the following code
can download the pre-trained model and data set. Set the `HTTP_PROXY` and `HTTPS_PROXY` environment variables to point
to your proxy server and port before launching python or jupyter.

```python
import numpy as np
from torchvision.io import read_image, ImageReadMode
from torchvision.models.detection import fasterrcnn_resnet50_fpn_v2, FasterRCNN_ResNet50_FPN_V2_Weights

# initialize object detection model from torchvision model zoo
weights = FasterRCNN_ResNet50_FPN_V2_Weights.DEFAULT
model = fasterrcnn_resnet50_fpn_v2(weights=weights)
model.eval()

# retrieve necessary image transformations (e.g., normalization, etc.) and available categories
preprocess = weights.transforms()
categories = np.array(weights.meta["categories"])
```

Note that the model is pre-trained on the MS COCO data set with several categories. In our example, we only
work with the categories "person", "bicycle", and "car". In the next step, download and extract
the [Demo Detection Data Set](https://thetishostedfiles.blob.core.windows.net/demofiles/thetis_demo_detection.zip) which is artificially generated using
the [Carla simulation engine](https://carla.org/). After download and extraction, we can load the JSON annotation
files and run inference with the Torchvision model:

```python
import os
from glob import glob
from tqdm import tqdm
import json
import torch

# set the inference device - if you have a CUDA device, you can set it to "cuda:<idx>"
device = "cpu"
# device = "cuda:0"

model.to(device)

# get a list of all JSON files
annotation_files = glob(os.path.join("demo_detection", "annotations", "*.json"))
data = []

# iterate over all JSON files and retrieve annotations
for filename in tqdm(annotation_files, desc="Running inference on images ..."):
    with open(filename, "r") as open_file:
        anns = json.load(open_file)

    # load respective image, run preprocessing (transformation) and finally run inference
    img = read_image(os.path.join("demo_detection", "img", anns["image_file"]), ImageReadMode.RGB)
    img = [preprocess(img).to(device=device)]

    # make inference and copy back to CPU (if CUDA device has been used for inference)
    with torch.no_grad():
        pred = model(img)[0]
        pred = {k: v.cpu() for k, v in pred.items()}

    # store predicted and target data for current frame
    data.append((pred, anns))
```
</details>

#### Expected Data Format for Object Detection

After loading the ground truth information and running inference using an AI model (see example above),
we must format our predictions and annotations in a way that can be ingested by Thetis. In object detection evaluation mode,
Thetis expects a Python dictionary for the predictions and annotations, where the keys represent the image identifiers
(e.g., image name) and the values represent the individual (predicted or ground truth) objects within a single frame.

```python
import pandas as pd

# Thetis expects a dictionary with image name as key and a pd.DataFrame with predicted information as value.
# A similar format is also expected for the ground truth annotations with extra sensitive attributes
# used for fairness evaluation. The field "__meta__" is always required with meta information for each frame.
annotations = {"__meta__": pd.DataFrame(columns=["width", "height"])}
predictions = {}

# iterate over all frames with predicted and target information
for pred, anns in data:

    # retrieve predicted labels, bounding boxes, and filter predictions by label
    predicted_labels = categories[pred["labels"].numpy()]
    predicted_boxes = pred["boxes"].numpy().reshape((-1, 4))
    target_boxes = np.array(anns["boxes"]).reshape((-1, 4))
    filter = np.isin(predicted_labels, ["person", "bicycle", "car"])
    filename = anns["image_file"]

    # add predicted information as pd.DataFrame
    predictions[filename] = pd.DataFrame.from_dict({
        "labels": predicted_labels[filter],
        "confidence": pred["scores"].numpy()[filter],
        "xmin": predicted_boxes[:, 0][filter],
        "ymin": predicted_boxes[:, 1][filter],
        "xmax": predicted_boxes[:, 2][filter],
        "ymax": predicted_boxes[:, 3][filter],
    })

    # add ground truth information also as pd.DataFrame with additional sensitive attributes
    annotations[filename] = pd.DataFrame.from_dict({
        "target": anns["classes"],
        "gender": anns["gender"],
        "age": anns["age"],
        "xmin": target_boxes[:, 0],
        "ymin": target_boxes[:, 1],
        "xmax": target_boxes[:, 2],
        "ymax": target_boxes[:, 3],
    })

    # some additional meta information such as image width and height are also required
    annotations["__meta__"].loc[filename] = [anns["image_width"], anns["image_height"]]
```

*Important*: The dictionary for the ground truth annotations requires a key `__meta__` which holds width and height
information for each image within the data set, provided as Pandas DataFrame. Note that the index of the entries within
this DataFrame must match with the keys (i.e. image identifiers) of the Python dictionaries.

#### Running AI Safety Evaluation with Thetis

Given your data is in the right format, simply call Thetis with the predictions, the ground truth information and the
prepared configuration file:

```python
from thetis import thetis

# finally, we can call the Thetis evaluation service similarly to the classification case
result = thetis(
    config="examples/demo_config_detection.yaml",
    annotations=annotations,
    predictions=predictions,
    output_dir="./output",
    license_file_path="examples/demo_license_detection.dat",
)
```

For details of Thetis configuration, see section [Configuration](https://efs-opensource.github.io/Thetis/configuration.html). 
For the current example, you can download the [demo configuration file](https://raw.githubusercontent.com/EFS-OpenSource/Thetis/main/examples/demo_config_detection.yaml)
from this repository or [click here](https://thetishostedfiles.blob.core.windows.net/demofiles/thetis_demo_detection.zip).

Thetis returns its findings, the final rating and recommendations for mitigation strategies as a JSON-like dictionary.
We capture the dictionary as `result` and can access the different evaluation aspects:

* `result[<task>]['rating_score']` for the rating score of the selected task (e.g., 'fairness' or 'uncertainty').
* `result[<task>]['recommendations']` for the recommendations to mitigate possible issues of the selected task.
* `result[<task>]['rating_enum']` for a categorization of the actual aspect into `'GOOD'`, `'MEDIUM'`,
  or `'BAD'` depending on the rating score.

Note that the remaining evaluation metrics are grouped by the specified IoU scores which are used for the matching
of predicted objects with ground truth ones (e.g., an IoU score of 0.5 might be used to decide if a prediction
has matched an existing ground truth object or not). In the configuration file, you can specify multiple IoU scores
that are taken into account for the final evaluation process.
