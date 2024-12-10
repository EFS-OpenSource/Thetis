.. _Configuration:

Configuration
=============

Thetis needs a YAML configuration file that specifies several aspects, e.g., the task, available classes, requested
evaluation aspects, etc. `Download an example configuration file <https://raw.githubusercontent.com/EFS-OpenSource/Thetis/refs/heads/main/examples/demo_config_classification.yaml>`__ or copy/paste the
following configuration file. An explanation for each configuration aspect can be found below.


Example configuration file
--------------------------

A YAML configuration structure for Thetis has the following general form:

.. code-block:: yaml

   # meta data of model predictions and dataset
   meta:

     model:
       name: "<model name>"
       revision: "<model revision>"

     dataset:
       name: "<dataset name>"
       revision: "r1"


   # Examination task. Can be one of: "classification" (binary/multi-class classification),
   # "detection" (image-based object detection) or "regression"
   task: "classification"

   # Language of the final report. Can be one of: "en", "de"
   language: "en"

   # Task-specific settings. Required and available fields depend on the selected task.
   task_settings:

     # List of distinct classes that can occur within the dataset (can only be set for classification or
     # object detection). If specified then this parameter cannot be empty.
     distinct_classes: ["no person", "person"]

     # In binary classification (when 'distinct_classes' has length of 2), you must specify a positive label out of
     # the list of available classes. This is important since you only give a single "confidence" for each prediction,
     # targeting the probability of the positive class. May only be specified for binary classification.
     binary_positive_label: "person"

     # Bounding-box format. Can be one of: "xyxy" (xmin, ymin, xmax, ymax), "xywh" (xmin, ymin, width, height),
     # or "cxcywh" (center x, center y, width, height).
     detection_bbox_format: "xyxy"

     # List with IoU scores used for object detection evaluation
     # Note: the IoU score "0.5" is always active for the evaluation. You can specify more IoU scores if you want
     detection_bbox_ious: [0.75]

     # String with bounding box matching strategy. Must be one of: "exclusive", "max".
     detection_bbox_matching: "exclusive"

     # Set to true if the bounding boxes are also inferred with a separate variance score (currently not supported)
     detection_bbox_probabilistic: false

     # In detection mode, it is possible to set a confidence threshold
     # to discard blurry predictions with low confidence
     detection_confidence_thr: 0.2

     # In detection mode it is possible to specify a tolerance zone outside image bounds within which clipping is applied. The boxes within these zones are 
     # clipped to the image dimensions. For boxes outside the specified tolerance, an error is raised instead.
     detection_bbox_clipping: 20%

   # Settings for the data evaluation routine
   data_evaluation:
     examine: true

   # Settings for the AI baseline performance evaluation (which should be always performed!)
   performance:
     examine: true

   # Settings for the evaluation of confidence calibration
   uncertainty:
     examine: true

     # Number of bins used for ECE calculation, required for classification and detection evaluation
     ece_bins : 20

     # During ECE/D-ECE computation, bins with a number of samples less than this threshold are ignored
     # Required for classification and detection evaluation
     ece_sample_threshold: 10

     # Number of bins used for D-ECE calculation (object detection), required for detection evaluation
     dece_bins: 5

   # Settings for the evaluation of model fairness
   fairness:
     examine: true

     # Specify sensitive attributes that are used for fairness evaluation. For each of these attributes,
     # you need to specify the classes for which the attributes are actually valid (out of the labels
     # within 'distinct_classes' list). You can also leave it empty or type "all" to mark validity for all classes.
     sensitive_attributes:
       gender: ["no person", "person"]
       age: "all"


General application settings
----------------------------

In the following, we give a detailed overview about all possible general configuration settings.

.. list-table:: Meta information settings describing the customer information, model properties, and used dataset.
   :widths: 35 10 55
   :header-rows: 1

   * - Key/Specifier
     - Dtype
     - Description
   * - :code:`meta/model/name`
     - string
     - Name of the AI model used to generate predictions.
   * - :code:`meta/model/revision`
     - string
     - Revision of the AI model used to generate predictions.
   * - :code:`meta/dataset/name`
     - string
     - Name of the dataset holding the ground truth information.
   * - :code:`meta/dataset/revision`
     - string
     - Revision of the dataset holding the ground truth information.


.. list-table:: General application settings
   :widths: 35 10 55
   :header-rows: 1

   * - Key/Specifier
     - Dtype
     - Description
   * - :code:`task`
     - string
     - Selection of the examination task. Can be one of: "classification" (binary/multi-class classification), "detection" (image-based object detection).
   * - :code:`language`
     - string
     - Language of the final evaluation report. Can be one of: "en" (US English), "de" (German).
   * - :code:`task_settings/distinct_classes`
     - list of int or string
     - List of distinct classes that can occur within the dataset. Only to be provided in case of Classification or Detection
   * - :code:`task_settings/binary_positive_label`
     - int or string
     - In binary classification (when 'distinct_classes' has length of 2), you must specify a positive label out of
       the list of available classes. This is important since you only give a single "confidence" for each prediction,
       targeting the probability of the positive class.
   * - :code:`task_settings/detection_bbox_format`
     - string
     - Bounding-box format of the provided boxes in object detection mode. Can be one of: "xyxy" (xmin, ymin, xmax, ymax),
       "xywh" (xmin, ymin, width, height), or "cxcywh" (center x, center y, width, height).
   * - :code:`task_settings/detection_bbox_ious`
     - list of float
     - List with IoU scores (in [0, 1] interval) used for object detection evaluation.
       Note: the IoU score "0.5" is always active for the evaluation. You can specify more IoU scores if you want.
   * - :code:`task_settings/detection_bbox_matching`
     - string
     - String with bounding box matching strategy within object detection evaluation. The strategy of matching the predicted bounding boxes
       with the ground truth ones must be either "exclusive," where each prediction and each ground truth are assigned to at most a single counterpart,
       or "max," with maximum/non-exclusive bounding box matching, where each ground truth object may have multiple predictions assigned to it.
       The default is "exclusive".
   * - :code:`task_settings/detection_bbox_probabilistic`
     - boolean
     - Currently not used.
   * - :code:`task_settings/detection_confidence_thr`
     - float
     - In detection mode, it is possible to set a confidence threshold (in [0, 1] interval) to discard blurry predictions with low confidence.
   * - :code:`task_settings/detection_bbox_clipping`
     - int
     - In detection mode, it is possible to specify a tolerance zone outside the image in case of boxes that are out of image bounds.
       This can be ommitted, in which case no clipping is applied and an error is raised if a box is out of image bounds.
       Alternatively, it can be set to relative(relative to image width and height)% ([0-100]%) or absolute values in px ([int]px). 
       These specify the dimensions outside the image, such that if any boxes extend into this tolerance zone, they will get clipped to the image dimensions. 
       If boxes exceed these tolerance zones no clipping will be applied, an error will be raised instead.

Configuration of safety evaluation
----------------------------------

.. list-table:: Configuration settings for dataset evaluation.
   :widths: 35 10 55
   :header-rows: 1

   * - Key/Specifier
     - Dtype
     - Description
   * - :code:`data_evaluation/examine`
     - boolean
     - Enables/disables the data evaluation for the final rating & reporting.

.. list-table:: Configuration settings for AI performance evaluation.
   :widths: 35 10 55
   :header-rows: 1

   * - Key/Specifier
     - Dtype
     - Description
   * - :code:`performance/examine`
     - boolean
     - Enables/disables the AI performance evaluation (e.g., accuracy, mAP, precision, recall, etc.) for the final reporting.

.. list-table:: Configuration settings for uncertainty evaluation (uncertainty calibration).
   :widths: 35 10 55
   :header-rows: 1

   * - Key/Specifier
     - Dtype
     - Description
   * - :code:`uncertainty/examine`
     - boolean
     - Enables/disables the uncertainty evaluation (uncertainty calibration, e.g., computation of the Expected Calibration Error (ECE)) for the final rating & reporting.
   * - :code:`uncertainty/ece_bins`
     - int
     - Number of bins used for the computation of the Expected Calibration Error (ECE), Maximum Calibration Error (MCE),
       and the respective reliability diagrams. The default value is 20.
   * - :code:`uncertainty/ece_sample_threshold`
     - int
     - Sample threshold used for the computation of the ECE, MCE, D-ECE, and the respective reliability diagrams to discard
       bins with an amount of samples below this threshold. Discarding bins with only a small amount of samples is
       recommended to stabilize the ECE/MCE computations. The default value is 10.
   * - :code:`uncertainty/dece_bins`
     - int
     - Number of bins used for the computation of the Decetion Expected Calibration Error (D-ECE) (object detection only)
       and the respective reliability diagrams. The D-ECE is the counterpart of the ECE for position-dependent calibration
       evaluation of object detection tasks. The default value is 5.

.. list-table:: Configuration settings for AI fairness evaluation.
   :widths: 35 10 55
   :header-rows: 1

   * - Key/Specifier
     - Dtype
     - Description
   * - :code:`fairness/examine`
     - boolean
     - Enables/disables the AI fairness evaluation for the final rating & reporting.
   * - :code:`fairness/sensitive_attributes/<label name>`
     - optional string or list of int/string
     - Specify one or multiple sensitive attributes (e.g., gender or age) that are used for fairness evaluation.
       The value of this entry is a list of target classes (given by "distinct_classes" parameter) for which the
       sensitive attribute is valid. For example, if "distinct_classes" specifies labels "person" and "car", a
       sensitive attribute for "gender" might only be valid for target label "person". If the attribute is valid for
       all specified target labels, you can also leave the value empty or pass "all".