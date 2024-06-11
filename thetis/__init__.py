#  ****************************************************************************
#  MLflow-compatible wrapper function for Thetis.
#
#  @copyright (c) 2023 e:fs TechHub GmbH. All rights reserved.
#  Dr.-Ludwig-Kraus-Straße 6, 85080 Gaimersheim, DE, https://www.efs-techhub.com
#  ****************************************************************************

"""
API Reference of Thetis
=======================

This is the API reference of the main entrance points for the Thetis toolbox.

.. autosummary::
   :toctree: _autosummary

   thetis
   thetis_mlflow

   read_json_with_pandas
   write_json_with_pandas

"""

from .io import read_json_with_pandas
from .io import write_json_with_pandas

from .service import thetis
from .mlflow import thetis_mlflow

name = "thetis"
__version__ = "0.2.1"
