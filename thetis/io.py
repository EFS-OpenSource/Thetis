#  ****************************************************************************
#  Module with IO functions used to read/write Thetis-compatible files.
#
#  @copyright (c) 2023 e:fs TechHub GmbH. All rights reserved.
#  Dr.-Ludwig-Kraus-Straße 6, 85080 Gaimersheim, DE, https://www.efs-techhub.com
#  ****************************************************************************

from typing import Dict

from thetiscore import read_json_with_pandas as read_core
from thetiscore import write_json_with_pandas as write_core


def read_json_with_pandas(json_filename: str) -> Dict:
    """
    Read a JSON dictionary from disk that might also contain references to external pd.DataFrames with
    additional data.

    Args:
        json_filename: str with the filename to the root JSON file.

    Returns:
        Dict with the content of the JSON file.
    """

    return read_core(json_filename=json_filename)


def write_json_with_pandas(
        json_like: Dict,
        filename: str,
):
    """
    Write a dictionary with pd.DataFrames as single entries to a JSON file.
    All data will be written to a single JSON file with JSON string representations of the provided pd.DataFrame
    instances.

    Args:
        json_like: Dict with the input dictionary with pd.DataFrame entries.
        filename: str with the filename to write.
    """

    return write_core(json_like=json_like, filename=filename)
