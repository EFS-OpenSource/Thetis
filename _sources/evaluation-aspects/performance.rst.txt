.. _Performance:

Prediction performance of the model
===================================

Thetis provides basic metrics that are commonly used for the AI evaluation process.

**Important:** Since the rating and evaluation of the baseline AI performance highly depend on the actual use case,
Thetis does not provide a rating score or recommendations on the AI performance metrics.

Classification
--------------

For binary and multi-class classification tasks, we compute several metrics which are commonly used
to evaluate the baseline performance of an AI algorithm. As the basis, we refer to the terms
*true positives* (TP, correctly identified samples with a positive label), *true negatives* (TN, correctly identified
samples with a negative label), *false positives* (FP, samples with a predicted positive label but true negative label),
and *false negatives* (FN, samples with a predicted negative label but true positive label).
In a multi-class scenario, if a metric is based on TP, TN, FP, or FN (e.g., precision or recall), we apply
macro-averaging, i.e., the metrics are computed for each class separately, using a one-vs-all scheme, and averaged
afterwards to yield single scores.
Currently, the following metrics are implemented:

* **Accuracy** directly estimates the probability that the model classifies an instance correctly for a given dataset. While this metric is intuitive, it depends on the base rate of occurrence for each class in the dataset and is not applicable if the base rates in the dataset do not represent the class distribution in the classifier's deployment domain (see `Wikipedia article about base rate fallacy <https://en.wikipedia.org/wiki/Base_rate_fallacy>`__).
* **Sensitivity**, also known as recall, quantifies the ability of the classifier to capture all positive instances correctly. It measures the proportion of true positive instances that are correctly identified out of all actual positive instances. Sensitivity is important for minimizing false negatives, ensuring that positive instances are not overlooked.
* **Precision** measures the accuracy of positive predictions, indicating the proportion of true positive predictions out of all positive predictions made by the classifier. It focuses on minimizing false positives, crucial in scenarios where incorrectly identifying positive instances carries significant consequences.
* **Matthews correlation coefficient (MCC)** is a metric used to evaluate the performance where different aspects are gathered within a single score. The metric ranges from -1 to +1, where a score of +1 indicates perfect predictions with no mistakes. A score of 0 suggests that the classifier's predictions are no better than random guessing, while a score of -1 indicates total disagreement between predictions and actual labels, with all predictions being incorrect.

In the context of binary classification, we also report the following metrics:

* **Specificity** complements sensitivity by measuring the classifier's ability to avoid false alarms in identifying negative instances. It quantifies the proportion of true negative instances that are correctly identified out of all actual negative instances. High specificity minimizes false positive errors, enhancing the classifier's ability to accurately identify negative instances.
* **Negative predictive value** assesses the reliability of negative predictions made by the classifier. It quantifies the proportion of true negative predictions out of all negative predictions made by the classifier. Negative predictive value is particularly relevant in scenarios where correctly identifying negative instances is crucial.
* **Informedness** measures the classifier's ability to make correct positive and negative predictions simultaneously. Informedness ranges from -1 to 1, where a score of 1 indicates perfect classification, 0 indicates random classification, and -1 indicates perfectly incorrect classification.
* **Markedness** evaluates the classifier's ability to correctly predict positive instances while avoiding false positives. Markedness also ranges from -1 to 1, with 1 representing perfect classification, 0 indicating random classification, and -1 representing perfect misclassification.

Although a computation of **specificity** and **negative predictive value** would also be possible in a multiclass scenario
(as averages over all given classes, similar to recall and precision), we report these metrics for binary classification only.
In binary classification, another expression for specificity and NPV would be "recall and precision for the negative class".
Hence, a comprehensive evaluation of the classifier must consider both values, so as not to ignore the negative class.
In a multiclass setting, recall and precision already cover the classifier's performance over all classes as macro-average.
We therefore deem the addition of specificity and NPV redundant for multiclass tasks.

When used in combination, these metrics provide a comprehensive evaluation of classifier performance. Precision and sensitivity focus on the performance of positive predictions, while specificity and negative predictive value assess the performance of negative predictions. By considering both positive and negative predictions, these metrics offer insights into different aspects of classifier performance, enabling informed decision-making in various applications.


Regression
----------

For regression tasks (estimation of a continuous target score), several metrics about the prediction performance
(estimation error) are computed as basic indicators to assess the model performance depending on the
actual use case.
The following metrics are currently implemented:

* Mean Absolute Error - mean of absolute errors over all samples.
* Median Absolute Error - median of absolute errors over all samples. This metric is more robust against outliers.
* Mean Squared Error - mean of squared errors over all samples.
* Root Mean Squared Error - root mean of squared errors over all samples.
* Mean Absolute Percentage Error - mean of absolute errors relative to the absolute target score. The idea of this
  metric is to denote the error relative to the target data range. However, note that this metric is not interpretable
  as a percentage score in a :math:`[0, 100]` interval and can be arbitrarily high when the target scores are small and
  the prediction error is large.
* Coefficient of Determination (R2) - also known as :math:`R^2` score which denotes the estimation error relative to
  the variance in the target scores. For more information, see
  `Coefficient of Determination <https://en.wikipedia.org/wiki/Coefficient_of_determination>`__.

Furthermore, a diagram about predicted vs. target scores as well as a diagram about the distribution of
residuals is also shown to give a visual representation of the estimation error.

Object detection
----------------

In the context of object detection, we utilize the following metrics:

* Precision - fraction of all correctly predicted objects (TP) over all predicted objects (TP and FP), so that :math:`\text{TP} / (\text{TP} + \text{FP})`.
* Recall - fraction of all correctly identified objects (TP) over all real existing objects (TP and FN), so that :math:`\text{TP} / (\text{TP} + \text{FN})`.
* Average Precision (AP) - the AP score is defined as the area under the precision-recall curve for a varying confidence threshold.
* F1 score - harmonic mean of the precision and recall with :math:`2 * (\text{precision} * \text{recall}) / (\text{precision} + \text{recall})`