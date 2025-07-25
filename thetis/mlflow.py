#  @copyright (c) 2024 e:fs TechHub GmbH. All rights reserved.
#  Dr.-Ludwig-Kraus-Straße 6, 85080 Gaimersheim, DE, https://www.efs-techhub.com
"""
This module provides an MLflow-compatible wrapper function for the Thetis evaluation toolkit.
"""

import os
from typing import Union, Optional, Tuple, Dict
import pandas as pd

from thetiscore import thetis_mlflow as thetiscore_mlflow


def thetis_mlflow(
        *,
        config: Union[str, os.PathLike, Dict],
        predictions: Union[pd.DataFrame, Dict[str, pd.DataFrame]],
        annotations: Union[pd.DataFrame, Dict[str, pd.DataFrame]],
        description: Dict[str, str] = None,
        mlflow_step: Optional[int] = None,
        predictions_perturbations: None = None,
        license_file_path: Union[str, os.PathLike] = None,
        license_xml_str: str = None,
        license_key_and_signature: Tuple[str, str] = None,
) -> Dict:
    """
    Main function for the Thetis evaluation toolkit with added MLflow logging support. Given a ground truth dataset and
    the respective predictions by an AI model, this function examines various aspects such as performance, uncertainty
    consistency, fairness, and robustness. It supports tasks like classification, detection, and regression.

    You can pass the current step count via 'mlflow_step' to this function. The step count will be passed to
    MLflow's 'log_metric' function. Refer to the documentation for more details on individual metrics.

    Note: You must provide one of the following arguments for license validation: `license_file_path`,
    `license_xml_str`, or `license_key_and_signature`.

    Metrics:
        The set of metrics passed to MLflow depends on the selection of evaluation tasks.
        The following metrics are passed to MLflow when running in **classification** mode:

        - :code:`performance/accuracy` - Classification accuracy.
        - :code:`performance/balanced_accuracy` - Balanced classification accuracy.
        - :code:`performance/precision` - Classification precision.
        - :code:`performance/recall` - Classification recall.
        - :code:`performance/f1` - Classification F1 score (harmonic mean of precision and recall).
        - :code:`uncertainty/rating_score` - Rating score of classification uncertainty quality/calibration.
        - :code:`uncertainty/ece` - Expected Calibration Error (ECE).
        - :code:`uncertainty/mce` - Maximum Calibration Error (MCE).
        - :code:`uncertainty/nll` - Negative Log Likelihood (NLL).
        - :code:`uncertainty/brier` - Brier Score (BS).
        - :code:`fairness/rating_score` - Rating score of classification fairness.
        - :code:`fairness/demographic_parity_difference_score` - Demographic parity difference.
        - :code:`fairness/equalized_odds_difference_score` - Equalized odds difference.
        - :code:`data_evaluation/rating_score` - Rating score of dataset quality.

        The following metrics are passed to MLflow when running in **detection** mode:

        - :code:`performance/iou_<IoU score>/ap` - Detection Average Precision for a certain IoU score.
        - :code:`performance/iou_<IoU score>/precision` - Detection precision for a certain IoU score.
        - :code:`performance/iou_<IoU score>/recall` - Detection recall for a certain IoU score.
        - :code:`performance/iou_<IoU score>/f1` - Detection F1 score (harmonic mean of precision and recall) for a
          certain IoU score.
        - :code:`uncertainty/rating_score` - Rating score of detection uncertainty quality/calibration.
        - :code:`uncertainty/iou_<IoU score>/ece` - Expected Calibration Error (ECE) for a certain IoU score.
        - :code:`uncertainty/iou_<IoU score>/dece_xy` - Detection Expected Calibration Error (D-ECE) which measures
          miscalibration w.r.t. cx/cy position for a certain IoU score.
        - :code:`uncertainty/iou_<IoU score>/dece_wh` - Detection Expected Calibration Error (D-ECE) which measures
          miscalibration width/height information for a certain IoU score.
        - :code:`uncertainty/iou_<IoU score>/mce` - Maximum Calibration Error (MCE) for a certain IoU score.
        - :code:`uncertainty/iou_<IoU score>/nll` - Negative Log Likelihood (NLL) for a certain IoU score.
        - :code:`uncertainty/iou_<IoU score>/brier` - Brier Score (BS) for a certain IoU score.
        - :code:`fairness/rating_score` - Rating score of detection fairness.
        - :code:`fairness/iou_<IoU score>/demographic_parity_difference_score` - Demographic parity difference
          for a certain IoU score.
        - :code:`data_evaluation/rating_score` - Rating score of dataset quality.

        Note: the computation of many metrics depends on the selected IoU scores. These metrics are given for any
        specified IoU score.

    Diagrams:
        The set of diagrams passed to MLflow depends on the selection of evaluation tasks.
        The following Matplotlib diagrams are passed to MLflow when running in **classification** mode:

        - :code:`performance/confusion_matrix_fig.svg` - Classification confusion matrix showing the fraction of
          correct and false predictions w.r.t. available classes.
        - :code:`uncertainty/uncertainty_reliability_diagram_fig.svg` - Reliability diagram in the context of
          uncertainty quality/calibration evaluation showing the miscalibration w.r.t. a certain confidence level.
        - :code:`fairness/selection_rate_diagram_<Sensitive Feature>_fig.svg` - Selection rate diagram showing the
          disparity in the selection rate (aka recall) w.r.t. a certain sensitive feature.
        - :code:`fairness/disparity_diagram_<Sensitive Feature>_fig.svg` - Performance disparity diagram showing
          the disparity in over-/underestimation w.r.t. a certain sensitive feature.
        - :code:`data_evaluation/cls_ratio_dataset_fig.svg` - Bar chart showing the label distribution of ground truth
          classes within the evaluation dataset.
        - :code:`data_evaluation/feature_<Sensitive Feature>_ratio_dataset_fig.svg` - Bar chart showing the label
          distribution of sensitive feature information within the evaluation dataset w.r.t. a certain sensitive
          feature.

        Note: the creation of some diagrams depends on the specified sensitive features (fairness evaluation).
        For multiple sensitive features, multiple diagrams are created.

        The following Matplotlib diagrams are passed to MLflow when running in **classification** mode:

        - :code:`performance/bar_chart_detection_performance_iou_<IoU score>_fig.svg` - Bar chart showing the detection
          performance metrics (precision, recall, AP) for each label within the dataset and for a certain IoU score.
        - :code:`performance/precision_recall_curve_iou_<IoU score>_fig.svg` - Precision-Recall curve for each label
          within the dataset and for a certain IoU score.
        - :code:`uncertainty/uncertainty_reliability_diagram_iou_<IoU score>_fig.svg`  - Reliability diagram in the
          context of uncertainty quality/calibration evaluation showing the miscalibration w.r.t. a certain
          confidence level for a certain IoU score.
        - :code:`uncertainty/uncertainty_reliability_diagram_xy_iou_<IoU score>_fig.svg` - Reliability diagram n the
          context of object detection uncertainty quality/calibration evaluation showing the miscalibration w.r.t.
          the **cx/cy** position of detected objects (as a heatmap) for a certain IoU score.
        - :code:`uncertainty/uncertainty_reliability_diagram_wh_iou_<IoU score>_fig.svg` - Reliability diagram n the
          context of object detection uncertainty quality/calibration evaluation showing the miscalibration w.r.t.
          the **width/height** position of detected objects (as a heatmap) for a certain IoU score.
        - :code:`fairness/selection_rate_diagram_<Sensitive Feature>_iou_<IoU score>_fig.svg` - Selection rate diagram
          showing the disparity in the selection rate (aka recall) w.r.t. a certain sensitive feature
          for a certain IoU score.
        - :code:`data_evaluation/target_data_distribution_fig.svg` - Heatmap showing the distribution of **real target**
          objects w.r.t. their cx/cy position.
        - :code:`data_evaluation/pred_data_distribution_fig.svg` - Heatmap showing the distribution of **predicted**
          objects w.r.t. their cx/cy position.
        - :code:`data_evaluation/feature_<Sensitive Feature>_ratio_dataset_fig.svg` - Bar chart showing the label
          distribution of sensitive feature information within the evaluation dataset w.r.t. a certain sensitive
          feature.

        Note: the computation of some diagrams depends on the selected IoU scores. These diagrams are drawn for any
        specified IoU score.

    Artifacts:
        The following artifacts are passed to MLflow:

        - :code:`thetis-result.json` - Thetis result JSON with all metrics and diagrams mentioned above.
        - :code:`report.pdf` - Thetis result PDF report with detailed rating scores, recommendations,
          metrics, and diagrams.

    Args:
        config: Application configuration options provided by the user.
        predictions: Predictions made by the AI model.
            **Classification:** DataFrame with columns "labels" and "confidence".
            **Detection:** Dict with DataFrame entries for each image, containing columns "labels", "confidence",
            and bounding box coordinates. The bounding box columns must correspond to the format specified in
            the user configuration.
            **Regression:** DataFrame with columns "predictions" and "stddev" (standard deviation).
        annotations: Ground truth data.
            **Classification:** DataFrame with columns "target" and optionally sensitive attributes.
            **Detection:** Dict with DataFrame entries for each image, containing columns "target", bounding box
            coordinates and optionally sensitive attributes. The bounding box columns must correspond to the format
            specified in the user configuration. Must also include a "__meta__" key with image metadata.
            **Regression:** DataFrame with columns "target" and optionally sensitive attributes.
         description: dict containing a description of your AI solution required for creating a technical documentation
            in accordance with Article 11 and Annex IV of the AI Act. The data entered here includes the title,
            provider, contact person (intern), contact person (extern), purpose, requirements, forms of distribution,
            hardware details and a UI description. These details cannot be automatically filled out and must be provided
            manually to ensure the documentation's completeness and transparency. If certain fields in the descriptions
            are not filled in, they also remain empty in the technical documentation.
        mlflow_step: Optional integer with the current step count to be passed to MLflow's "log_param" function.
        predictions_perturbations: AI predictions for each configured perturbation type.
            The perturbation type is the key of the dictionary, and each value must have the same format as the "predictions" parameter.
        license_file_path: Path to an XML license file to run the application.
        license_xml_str: String representation of an XML license file to run the application.
        license_key_and_signature: Tuple of license key and signature strings.

    Returns:
        Dictionary with the evaluation results, rating scores, and recommendations for the examined AI model.

    Raises:
        RuntimeError: if license_file_path is given but file path is malformed
            (e.g., due to insufficient escaping of backslashes).
        RuntimeError: if neither 'license_file_path', 'license_xml_str', 'license_key_and_signature', THETIS_LICENSE,
            "license.dat" in working directory nor "license.dat" in user local home directory (OS specific)
            could be found.
        RuntimeError: if the license Key XML cannot be parsed.
        RuntimeError: if the license Key XML cannot be parsed.
        RuntimeError: if config is given as file path but file path is malformed
            (e.g., due to insufficient escaping of backslashes).
        RuntimeError: if the given language identifier is unknown or not supported.
        RuntimeError: if the indices of the predicted and ground truth dataset do not match to each other
            (classification or regression).
        RuntimeError: if the arrays for predicted labels and ground truth dataset have different dtypes.
        RuntimeError: if multi-class extraction failed and if more than 2 distinct classes are detected.
        RuntimeError: if multi-class extraction failed and if the specified positive label within the application
            config cannot be found in the dataset (binary classification).
        RuntimeError: if bbox_format is not one of 'xyxy', 'xywh', or 'cxcywh'.
        RuntimeError: if uncertainty evaluation is active but no uncertainty information is given (regression).
        FileNotFoundError: if file with given license_file_path cannot be found.
        FileNotFoundError: if config is given as file path but no appropriate file can be found.
        AttributeError: if the key 'Key' cannot be found at the expected location.
        AttributeError: if the key 'Signature' cannot be found at the expected location.
        AttributeError: if the key 'ExpiryDate' cannot be found at the expected location.
        AttributeError: if classification or detection mode but key "distinct_classes" is missing or empty.
        AttributeError: if classification mode but length of "distinct_classes" is lower than 2.
        AttributeError: if binary classification mode (length of "distinct_classes" is 2) but error_msg field
            "binary_positive_label" is missing.
        AttributeError: if detection mode but key "task_settings/detection_bbox_format" is missing in user config.
        AttributeError: if "fairness" evaluation is active but no sensitive feature has been specified.
        AttributeError: if the key 'Features' cannot be found at the expected location.
        AttributeError: if the requested column "labels" does not exist within the predicted dataset
            (classification or detection).
        AttributeError: if the requested column "predictions" does not exist within the predicted dataset (regression).
        AttributeError: if the requested column "target" does not exist within the ground truth dataset.
        AttributeError: if multi-class extraction failed and if the requested column "confidence" does not exist within
            the predicted dataset (binary classification or detection).
        AttributeError: if a sensitive feature is defined for a label that has not been found in the dataset.
        AttributeError: if the requested column for a sensitive feature does not exist within the ground truth dataset.
        AttributeError: if the field '__meta__' within the ground truth dataset annotations is completely missing.
        AttributeError: if the meta information provided by '__meta__' is missing for a certain image.
        ValueError: if "distinct_classes" in application config contains duplicates (classification or detection).
        ValueError: if the data type conversion to one of "int" or "str" of column "labels" failed
            (classification or detection).
        ValueError: if the data type conversion to "float" of column "predictions" failed (regression).
        ValueError: if the data type conversion to one of "int" or "str" of column "target" failed
            (classification or detection).
        ValueError: if the data type conversion to "float" of column "target" failed (regression).
        ValueError: if column "variance" exists in predictions dataframe and if the data type conversion
            to "float" of column "variance" failed (regression).
        ValueError: if column "stddev" exists in predictions dataframe and if the data type conversion
            to "float" of column "stddev" failed (regression).
        ValueError: if classes are found that have not been specified by 'distinct_classes' in the config file.
        ValueError: if binary classification and "binary_positive_label" can not be found in "distinct_classes".
        ValueError: if multi-class extraction failed and if the data type conversion to "float" of column "confidence"
            failed within the predicted dataset (binary classification or detection).
        ValueError: if the data type conversion to one of "int" or "str" failed for a requested sensitive feature
            within the ground truth dataset.
        ValueError: if a sensitive feature has a missing or invalid entry.
        ValueError: if a sensitive feature has less than 2 distinct labels.
        ValueError: if the image width or height information provided by '__meta__' for a certain image are <= 0.
        ValueError: if bbox_format is 'xyxy' and xmin > xmax (detection).
        ValueError: if bbox_format is 'xyxy' and ymin > ymax (detection).
        ValueError: if bbox_format is 'xywh' or 'cxcywh' and width is negative (detection).
        ValueError: if bbox_format is 'xywh' or 'cxcywh' and height is negative (detection).
        NotImplementedError: if task is not one of "classification", "regression", or "detection".
        NotImplementedError: if the bounding box matching strategy is not one of "exclusive", "max".
        TypeError: if config is neither str nor python dict.
        TypeError: if 'predictions' is not type pd.DataFrame (classification or regression).
        TypeError: if 'annotations' is not type pd.DataFrame (classification or regression).
        TypeError: if 'predictions' is not type dict (detection).
        TypeError: if any value in 'predictions' dictionary is not type pd.DataFrame (detection).
        TypeError: if 'annotations' is not type dict (detection).
        TypeError: if any value in 'annotations' dictionary is not type pd.DataFrame (detection).
        TypeError: if 'description' is not type dict
        TypeError: if 'description' values are not type str
        KeyError: if 'description' has unexpected or missing keys
        SyntaxError: if the provided configuration file is not in proper YAML format.
        SyntaxError: if the syntax of the user configuration is malformed according to
            the required configuration schema.
        thetiscore.errors.LicenseInvalidError: if the passed license key/signature pair is invalid.
        thetiscore.errors.LicenseExpiredError: if the license has expired.
        thetiscore.errors.TaskNotLicensedError: if a task is requested by the user which has not been licensed.
        thetiscore.errors.ThetisInternalLicenseError: if an unexpected application error during
            license verification occurred.
        thetiscore.errors.ThetisInternalError: if an unexpected application error occurred.
    """

    return thetiscore_mlflow(
        config=config,
        predictions=predictions,
        annotations=annotations,
        description=description,
        mlflow_step=mlflow_step,
        predictions_perturbations=predictions_perturbations,
        license_file_path=license_file_path,
        license_xml_str=license_xml_str,
        license_key_and_signature=license_key_and_signature,
    )
