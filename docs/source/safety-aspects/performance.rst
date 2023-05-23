.. _Performance:

AI Performance Metrics
======================

Thetis is able to provide basic metrics that are commonly used for the AI evaluation process.

**Important:** since the rating and evaluation of the baseline AI performance highly depends on the actual use case,
Thetis does not provide a rating score or recommendations on the AI performance metrics.

Classification
--------------

For binary and multi-class classification tasks, we compute the several metrics which are commonly used
to evaluate the baseline performance of an AI algorithm. As the basis, we refer to the terms of
*true positives* (TP, correctly identified samples with positive label), *true negatives* (TN, correctly identified
samples with negative label), *false positives* (FP, samples with predicted positive label but true negative label),
and *false negatives* (FN, samples with predicted negative label but true positive label).
In a multi-class scenario, if a metric is based on TP, TN, FP, or FN (e.g., precision or recall), we apply
micro-averaging, i.e., the metrics are computed globally by counting the total TP, TN, FP, or FN.
Currently, the following metrics are implemented:

* Accuracy - fraction of correctly predicted samples over all samples.
* Balanced Accuracy - similar to the standard accuracy but reweighted according to the class distribution. This should avoid inflated performance estimates on imbalanced data sets. For more information, see `Scikit-Learn Balanced Data Set <https://scikit-learn.org/stable/modules/model_evaluation.html#balanced-accuracy-score>`__.
* Precision - fraction of all correctly identified positives (TP) over all samples with predicted positive label (TP and FP), so that :math:`\text{TP} / (\text{TP} + \text{FP})`.
* Recall - fraction of all correctly identified positives (TP) over all samples that should have been predicted as positive (TP and FN), so that :math:`\text{TP} / (\text{TP} + \text{FN})`.
* F1 score - harmonic mean of the precision and recall with :math:`2 * (\text{precision} * \text{recall}) / (\text{precision} + \text{recall})`

Regression
----------

Coming soon.

Object Detection
----------------

In the context of object detection, we utilize the following metrics:

* Precision - fraction of all correctly predicted objects (TP) over all predicted objecs (TP and FP), so that :math:`\text{TP} / (\text{TP} + \text{FP})`.
* Recall - fraction of all correctly identified objects (TP) over all real existing objects (TP and FN), so that :math:`\text{TP} / (\text{TP} + \text{FN})`.
* Average Precision (AP) - the AP score is defined as the area under the precision-recall curve for a varying confidence threshold.
* F1 score - harmonic mean of the precision and recall with :math:`2 * (\text{precision} * \text{recall}) / (\text{precision} + \text{recall})`