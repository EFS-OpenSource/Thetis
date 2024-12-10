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
* <platform tag> describes the platform for which the application has been built (e.g, "manylinux" works for most Unix-based systems).


Getting started
---------------

To get started with Thetis, follow these steps:

1. **Prepare your environment:**
   Ensure you have a Python environment set up. Install Thetis using the instructions provided above.

2. **Explore examples:**
   Review our :doc:`usage examples <examples>` to understand how to use Thetis for different AI tasks.

3. **Run your analysis:**
   Integrate your AI model and data with Thetis, then perform the desired analysis. Refer to the detailed
   :doc:`API documentation <api>` and :doc:`configuration options <configuration>` for more information.
   Note that in the free version, only a reduced set of evaluation aspects is supported. If you need the full
   functionalities, a valid license is required.
   Please reach out to us via `thetis@efs-techhub.com <mailto:thetis@efs-techhub.com>`__.


Issues & bugtracking
--------------------

If you experience any issues during installation, running, or handling Thetis, please create an issue on the
`e:fs Github page <https://github.com/efs-OpenSource/thetis>`__ and post the provided stack trace.
