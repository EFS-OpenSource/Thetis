![Thetis Logo](https://github.com/EFS-OpenSource/Thetis/blob/main/docs/source/_static/thetis-logo.png?raw=true)


_Even if your AI is as strong as Achilles, Thetis will certainly know about its weaknesses._

---

**Thetis** is our comprehensive solution for AI system analysis, ensuring that AI applications remain safe, reliable, and ethical. Designed with regulatory requirements like the AI Act of the European Union in mind, Thetis provides detailed findings and analytics, offering key insights to support your auditing and QA processes.

Thetis evaluates various aspects of AI systems, including performance, uncertainty consistency (calibration), fairness, and robustness. It also assesses the quality of your datasets, alerting you to potential hidden issues. Thetis supports a wide range of AI tasks, such as detection, classification, and regression.

This repository and README serve as a technical user guide for engineers. If you are a legal professional or a compliance officer, visit our [product page](https://www.efs-techhub.com/efs-portfolio/loesungen/thetis) (in German) to discover how Thetis can enhance the safety, reliability, and ethical standards of your AI applications.

For detailed documentation and technical background on all analysis modes and features, visit the [API Documentation Page](https://efs-opensource.github.io/Thetis/index.html).

## Installation

As a python package, Thetis is installed from the Python Package Index (PyPI) using Python's installer _pip_. Within your python environment, simply type:

```shell
$ pip install thetis
```

This will install the latest available version of Thetis and all its dependencies.

## Obtaining a license

The [usage examples](https://github.com/EFS-OpenSource/Thetis/blob/main/examples/README.md) in this repository come with free demo licenses tied to each example. To try Thetis with your own data or to obtain a professional license, please contact us at [efs-techhub.com](https://efs-techhub.com/efs-portfolio/loesungen/thetis).

Thetis will automatically detect your license file if it is placed in your working directory or at the following locations:

* Windows: `<User>\\AppData\\Local\\Thetis\\license.dat`
* Unix: `~/.local/thetis/license.dat`

Alternatively, you can specify the license location as a parameter when calling Thetis.

## Quickstart

We have prepared [several examples](https://github.com/EFS-OpenSource/Thetis/blob/main/examples/README.md) to demonstrate Thetis's capabilities and help you get started with your own model data analysis. Depending on your use case, refer to the following examples:

* [Detection task example](https://github.com/EFS-OpenSource/Thetis/blob/main/examples/detection.ipynb)
* [Classification task example](https://github.com/EFS-OpenSource/Thetis/blob/main/examples/classification.ipynb)
* [Regression task example](https://github.com/EFS-OpenSource/Thetis/blob/main/examples/regression.ipynb)

## Get in touch

If you have any questions, would like to schedule a personal demo, or wish to provide feedback, please contact us at [efs-techhub.com](https://efs-techhub.com/efs-portfolio/loesungen/thetis).