![Thetis Logo](https://github.com/EFS-OpenSource/Thetis/blob/main/docs/source/_static/thetis-logo.png?raw=true)


_Even if your AI is as strong as Achilles, Thetis will certainly know about its weaknesses._

---

### Checkout our new [online dashboard](https://app.thetis.de/) for Thetis and register for free!

---

**Thetis** is our comprehensive solution for AI system analysis, ensuring that AI applications remain safe, reliable, and ethical. Designed with regulatory requirements like the AI Act of the European Union in mind, Thetis provides detailed findings and analytics, offering key insights to support your auditing and QA processes.

Thetis evaluates various aspects of AI systems, including performance, uncertainty consistency (calibration), fairness, and robustness. It also assesses the quality of your datasets, alerting you to potential hidden issues. Thetis supports a wide range of AI tasks, such as detection, classification, and regression.

This repository and README serve as a technical user guide for engineers. If you are a legal professional or a compliance officer, visit our [product page](https://thetis.de) (in German) or directly [try out Thetis online](https://app.thetis.de/) to discover how Thetis can enhance the safety, reliability, and ethical standards of your AI applications.

For detailed documentation and technical background on all analysis modes and features, visit the [API Documentation Page](https://efs-opensource.github.io/Thetis/index.html).

## Installation

As a python package, Thetis is installed from the Python Package Index (PyPI) using Python's installer _pip_. Within your python environment, simply type:

```shell
$ pip install thetis
```

This will install the latest available version of Thetis and all its dependencies.

## Usage and obtaining a license

The core functions of Thetis are free to use. If you wish to conduct deeper investigations of your AI application, you
can easily apply for a license. [Send us a mail](mailto:thetis@efs-techhub.com) and we will reach out to you soon!

The [usage examples](https://github.com/EFS-OpenSource/Thetis/blob/main/examples) in this repository come with free demo licenses tied to each example. These examples demonstrate the full functionalities of Thetis.

Thetis will automatically detect your license file if it is placed in your working directory or at the following locations:

* Windows: `<User>\\AppData\\Local\\Thetis\\license.dat`
* Unix: `~/.local/thetis/license.dat`

Alternatively, you can specify the license location as a parameter when calling Thetis.

## Quickstart

We have prepared [several examples](https://github.com/EFS-OpenSource/Thetis/blob/main/examples/README.md) to demonstrate Thetis's capabilities and help you get started with your own model data analysis. Depending on your use case, refer to the following examples:

* [Classification task example](https://github.com/EFS-OpenSource/Thetis/blob/main/examples/classification.ipynb)
* [Detection task example](https://github.com/EFS-OpenSource/Thetis/blob/main/examples/detection.ipynb)
* [Regression task example](https://github.com/EFS-OpenSource/Thetis/blob/main/examples/regression.ipynb)

## Get in touch

If you have any questions, would like to schedule a personal demo, or wish to provide feedback, please contact us via mail at [thetis@efs-techhub.com](mailto:thetis@efs-techhub.com).

## Terms of Use

The terms of use of Thetis can be found at [https://app.thetis.de/static/terms](https://app.thetis.de/static/terms).
A detailed description of our packages and system requirements can be found at [https://app.thetis.de/download/Leistungsbeschreibung.pdf](https://app.thetis.de/download/Leistungsbeschreibung.pdf) (in German).
