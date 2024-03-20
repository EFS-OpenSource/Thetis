#  ****************************************************************************
#  Main service for tha Thetis evaluation toolbox.
#
#  @copyright (c) 2023 e:fs TechHub GmbH. All rights reserved.
#  Dr.-Ludwig-Kraus-Straße 6, 85080 Gaimersheim, DE, https://www.efs-techhub.com
#  ****************************************************************************

import os
from typing import Union, Optional, Tuple, Dict
import pandas as pd

from thetiscore import thetis as thetiscore_main


def thetis(
        *,
        config: Union[str, os.PathLike, Dict],
        predictions: Union[pd.DataFrame, Dict[str, pd.DataFrame]],
        annotations: Union[pd.DataFrame, Dict[str, pd.DataFrame]],
        output_dir: Optional[str] = None,
        predictions_perturbations: Optional[Dict[str, Union[pd.DataFrame, Dict[str, pd.DataFrame]]]] = None,
        license_file_path: Union[str, os.PathLike] = None,
        license_xml_str: str = None,
        license_key_and_signature: Tuple[str, str] = None,
        return_svg: Optional[bool] = False,
) -> Dict:
    """
    Main entrance point for the Thetis evaluation service. Given a ground truth data set and the respective
    predictions by an AI model, this service examines several safety-relevant aspects such as uncertainty quality,
    data set quality, performance metrics, and fairness.

    Args:
        config: dict with application configuration options provided by the user.
        predictions: If task is "classification", pd.DataFrame representing the AI output on the ground truth data
            set. Expected columns: "labels", "confidence", and bounding box information for object detection.
            if task is "detection", Dict with pandas DataFrames representing the predictions of an AI model for each
            image. The dict keys are the image identifiers.
            Expected fields in the dictionary: entries (pd.DataFrame) for each image with
            columns "confidence" and bounding box information according to the specified bounding box format.
        annotations: If task is "classification", pd.DataFrame representing the ground truth data set.
            Expected columns: "target", sensitive feature, and bounding box information for object detection.
            If task is "detection", Dict with pandas DataFrames representing the ground truth annotations for
            each image. The dict keys are the image identifiers.
            Expected fields in the dictionary: "__meta__" with data set meta information and
            entries (pd.DataFrame) for each image with columns "target" and bounding box information according
            to the specified bounding box format.
        output_dir: str with path to the output directory where the PDF report will be stored in.
            Set this to None (default) to disable PDF report creation.
        predictions_perturbations: Dict with AI predictions for each configured perturbation type.
            The perturbation type is the key of the dictionary, whereas each value must have the same format
            as the "predictions" parameter.
        license_file_path: os.PathLike pointing to an XML license file to run the application.
            Either 'license_file_path', 'license_xml_str', or 'license_key_and_signature' must be given.
        license_xml_str: str with already read string representing the content of an XML license file to run the
            application. Either 'license_file_path', 'license_xml_str', or 'license_key_and_signature' must be given.
        license_key_and_signature: Tuple of two strings with already read license key and license signature as strings.
            Either 'license_file_path', 'license_xml_str', or 'license_key_and_signature' must be given.
        return_svg: boolean flag which enables/disables returning Matplotlib (SVG) figures. Default is False to filter
            out these figures as they cannot be serialized in plain JSON format. Set to True explicitly if
            you want to obtain the figures directly.

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
        RuntimeError: if the indices of the predicted and ground truth data set do not match to each other
            (classification or regression).
        RuntimeError: if the arrays for predicted labels and ground truth data set have different dtypes.
        RuntimeError: if multi-class extraction failed and if more than 2 distinct classes are detected.
        RuntimeError: if multi-class extraction failed and if the specified positive label within the application
            config cannot be found in the data set (binary classification).
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
        AttributeError: if the requested column "labels" does not exist within the predicted data set
            (classification or detection).
        AttributeError: if the requested column "predictions" does not exist within the predicted data set (regression).
        AttributeError: if the requested column "target" does not exist within the ground truth data set.
        AttributeError: if multi-class extraction failed and if the requested column "confidence" does not exist within
            the predicted data set (binary classification or detection).
        AttributeError: if a sensitive feature is defined for a label that has not been found in the data set.
        AttributeError: if the requested column for a sensitive feature does not exist within the ground truth data set.
        AttributeError: if the field '__meta__' within the ground truth data set annotations is completely missing.
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
            failed within the predicted data set (binary classification or detection).
        ValueError: if the data type conversion to one of "int" or "str" failed for a requested sensitive feature
            within the ground truth data set.
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

    return thetiscore_main(
        config=config,
        predictions=predictions,
        annotations=annotations,
        output_dir=output_dir,
        predictions_perturbations=predictions_perturbations,
        license_file_path=license_file_path,
        license_xml_str=license_xml_str,
        license_key_and_signature=license_key_and_signature,
        return_svg=return_svg,
    )
