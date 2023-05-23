.. _Installation:

Installation
============

Thetis is installed via the Python Package Index (PyPI) using Python's PIP-Tool. Simply type

.. code-block:: shell

     $ pip install thetis

to install the right version of Thetis in your Python environment. The installer will directly choose
the right wheel for installation.

You can also download a `pre-built Wheel of Thetis <https://pypi.org/project/thetis/#files>`__ and install it
afterwards in your Python environment by typing

.. code-block:: shell

     $ pip install <download folder>/thetis-<thetis version>-py3-<python tag>-<abi tag>-<platform tag>.whl

In this case, the user is responsible to download the right wheel for the desired Thetis version and the
runtime environment that is used during application execution:

* <thetis version> describes the desired application version of Thetis.
* <python tag> describes the Python version which has been used for building the wheel (e.g., "cp38" stands for Python version 3.8).
* <abi tag> describes the Application Binary Interface (ABI) version for which the wheel has been built (e.g., "cp38" stands for Python version 3.8).
* <platform tag> describes the platform for which the application has been built (e.g, "linux_x86_64" stands for a Linux OS on a x86 architecture with a 64 bit system).

Issues & Bugtracking
====================

If you experience any issues during installation, running, or handling Thetis, please create an issue on
`e:fs Github page <https://github.com/efs-OpenSource/thetis>`__.
