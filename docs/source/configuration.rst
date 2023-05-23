.. _Configuration:

Configuration
=============

Thetis needs a YAML configuration file that specifies several aspects, e.g., the task, available classes, requested
evaluation aspects, etc. `Download an exemplary configuration file <https://efs-techhub.com>`__ or copy/paste the
following configuration file. An explanation for each configuration aspect can be found below.


Example Configuration File
--------------------------

An exemplary YAML configuration for Thetis must have the following form:

.. code-block:: yaml

   # meta data: issuer, address, etc.
   meta:

     company:
       company_name: "Example Company Ltd."
       company_street: "Example Street 3"
       company_postal: "12345"
       company_city: "Example Village"
       company_country: "Germany"

     model:
       name: "<model name>"
       revision: "<model revision>"
       hash: "<some hash retrieved by AI model>"

     dataset:
       name: "<data set name>"
       revision: "r1"


   # examination task. Can be one of: "classification" (binary/multi-class classification),
   # "detection" (image-based object detection)
   task: "classification"

   # language of the final report. Can be one of: "en", "de"
   language: "en"

   # list of distinct classes that can occur within the data set
   distinct_classes: ["no person", "person"]

   # in binary classification (when 'distinct_classes' has length of 2), you must specify a positive label out of
   # the list of available classes. This is important since you only give a single "confidence" for each prediction,
   # targeting the probability of the positive class
   binary_positive_label: "person"

   # you can specify some general settings here (atm only detection-specific settings)
   task_settings:

     # bounding-box format. Can be one of: "xyxy" (xmin, ymin, xmax, ymax), "xywh" (xmin, ymin, width, height),
     # or "cxcywh" (center x, center y, width, height).
     detection_bbox_format: "xyxy"

     # list with IoU scores used for object detection evaluation. Common choices are "0.5" and/or "0.75".
     detection_bbox_ious: [0.5, 0.75]

     # set to true if the bounding boxes are also inferred with a separate variance score (currently not supported)
     detection_bbox_probabilistic: false

     # in detection mode, it is possible to set a confidence threshold
     # to discard blurry predictions with low confidence
     detection_confidence_thr: 0.2

   # settings for the data evaluation routine
   data_evaluation:
     examine: true

   # settings for the AI baseline performance evaluation (which should be always performed!)
   performance:
     examine: true

   # settings for the evaluation of confidence calibration
   uncertainty:
     examine: true

     # number of bins used for ECE calculation, required for classification and detection evaluation
     ece_bins : 20

     # during ECE/D-ECE computation, bins with a number of samples less than this threshold are ignored
     # required for classification and detection evaluation
     ece_sample_threshold: 10

     # number of bins used for D-ECE calculation (object detection), required for detection evaluation
     dece_bins: 5

     # number of quantiles used for Pinball/QCE computation, required for regression and probabilistic
     # detection evaluation (currently not supported)
     evaluation_quantiles: 11

   # settings for the evaluation of model fairness
   fairness:
     examine: true

     # specify sensitive attributes that are used for fairness evaluation. For each of these attributes,
     # you need to specify the classes for which the attributes are actually valid (out of the labels
     # within 'distinct_classes' list). You can also type "all" to mark validity for all classes.
     gender: ["no person", "person"]
     age: "all"


General Application Settings
----------------------------

In the following, we give a detailed overview about all possible general configuration settings.

.. list-table:: Meta information settings describing the customer information, model properties, and used data set.
   :widths: 35 10 55
   :header-rows: 1

   * - Key/Specifier
     - Dtype
     - Description
   * - :code:`meta/company/company_name`
     - string
     - Name of the company running the evaluation.
   * - :code:`meta/company/company_street`
     - string
     - Address street of the company running the evaluation.
   * - :code:`meta/company/company_postal`
     - string
     - Address postal of the company running the evaluation.
   * - :code:`meta/company/company_city`
     - string
     - Address city of the company running the evaluation.
   * - :code:`meta/company/company_country`
     - string
     - Address country of the company running the evaluation.
   * - :code:`meta/model/name`
     - string
     - Name of the AI model used to generate predictions.
   * - :code:`meta/model/revision`
     - string
     - Revision of the AI model used to generate predictions.
   * - :code:`meta/model/hash`
     - string
     - Hash of the AI model used to generate predictions.
   * - :code:`meta/dataset/name`
     - string
     - Name of the data set holding the ground-truth information.
   * - :code:`meta/dataset/revision`
     - string
     - Revision of the data set holding the ground-truth information.


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
   * - :code:`distinct_classes`
     - list of int or string
     - List of distinct classes that can occur within the data set.
   * - :code:`binary_positive_label`
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
     - List with IoU scores (in [0, 1] interval) used for object detection evaluation. Common choices are "0.5" and/or "0.75".
   * - :code:`task_settings/detection_bbox_probabilistic`
     - boolean
     - Currently not used.
   * - :code:`task_settings/detection_confidence_thr`
     - float
     - In detection mode, it is possible to set a confidence threshold (in [0, 1] interval) to discard blurry predictions with low confidence.

Configuration of Safety Evaluation
----------------------------------

.. list-table:: Configuration settings for data set evaluation.
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
   * - :code:`uncertainty/evaluation_quantiles`
     - int
     - Number of quantiles used for Pinball/QCE computation, required for regression and probabilistic detection
       evaluation (currently not supported).

.. list-table:: Configuration settings for AI fairness evaluation.
   :widths: 35 10 55
   :header-rows: 1

   * - Key/Specifier
     - Dtype
     - Description
   * - :code:`fairness/examine`
     - boolean
     - Enables/disables the AI fairness evaluation for the final rating & reporting.
   * - :code:`fairness/<label name>`
     - string or list of int/string
     - Specify one or multiple sensitive attributes (e.g., gender or age) that are used for fairness evaluation.
       The value of this entry is a list of target classes (given by "distinct_classes" parameter) for which the
       sensitive attribute is valid. For example, if "distinct_classes" specifies labels "person" and "car", a
       sensitive attribute for "gender" might only be valid for target label "person". If the attribute is valid for
       all specified target labels, you can also pass the value "all".