.. _Fairness:

Fairness
========

The evaluation of fairness of an AI algorithm is highly important to assess for a possible discrimination of
individual sensitive groups. Thetis evaluates for *group fairness* which evaluates the risk for individual groups of
experiencing discrimination. The fairness rating of an AI model is based on several fairness metrics which are
described in the following.

Classification
--------------

Given an input :math:`X \in \mathcal{X}`, a classification model :math:`h(X)` makes predictions
:math:`\hat{Y} \in \mathcal{Y}` targeting the ground truth label :math:`\bar{Y} \in \mathcal{Y}`, so that
:math:`h: \mathcal{X} \rightarrow \mathcal{Y}`. Furthermore, let :math:`A \in \mathcal{A}` denote a sensitive attribute
(e.g., attribute *gender*) for each :math:`X`. For baseline classifier evaluation, we can determine
the *true positives* (TP, correctly identified samples with positive label), *true negatives* (TN, correctly identified
samples with negative label), *false positives* (FP, samples with predicted positive label but true negative label),
and *false negatives* (FN, samples with predicted negative label but true positive label). From these scores, it is possible
to obtain the metrics *sensitivity (recall)* and *precision*, as well as *specificity* and *negative predictive value*
for binary classification tasks, respectively.

Now we want to compare the classifier performance by means of sensitive attribute :math:`A` and evaluate if there exists
any disparity in performance for different labels of attribute :math:`A` (e.g., a possible performance disparity
for labels *male*/*female* of attribute *gender*). The comparison is achieved by computing the aforementioned metrics
for each label separately, which is denoted by :math:`\text{sens}_a`, :math:`\text{spec}_a`,
:math:`\text{prec}_a`, and :math:`\text{neg}_a` in the following for sensitivitiy, specificity, precision, and
negative predictive value, respectively.

**Minimum ratio**: For each of these metrics, Thetis reports the minimum ratio between the group with lowest and
highest score, grouped by the labels of :math:`A`, which is denoted by

.. math::
   \frac{\min_{a \in \mathcal{A}} \text{metric}_a}
   {\max_{a \in \mathcal{A}} \text{metric}_a} ,

where :math:`\text{metric}_a` represents the considered metric.

Inspecting the ratio between minimum and maximum value quantifies the **relative** disparity between
individual groups. Using ratios instead of absolute differences allows us to handle cases with low baseline performance. For example, consider sensitive
attribute *gender* with labels *male* and *female* and a classifier that yields a sensitivity of
:math:`0.025` for label *female* and :math:`0.05` for label *male*. While the absolute difference between
sensitivity scores is only :math:`0.025`, the classifier still achieves twice the sensitivity for label *male*.

**Maximum difference**: In contrast, when the **absolute** disparity between individual groups is of interest, Thetis
also reports the maximum difference between the metric with highest score and the metric with lowest score,
computed for each label of :math:`A` separately, which is denoted by

.. math::
   \max_{a \in \mathcal{A}} \text{metric}_a - \min_{a \in \mathcal{A}} \text{metric}_a ,

where :math:`\text{metric}_a` represents the considered metric.

**Metric interpretation**: The ratios/differences for each of the aforementioned metrics can be interpreted as follows:

* **Sensitivity (Recall)**: Large relative or absolute differences in sensitivity indicate that the classifier performs better in recognizing positive samples for some sensitive groups than for other groups. This may be due to learned imbalances in the dataset, a general lack of training data for some groups, or an inherent correlation between sensitive groups and classification difficulty.
* **Precision**: A significant relative or absolute difference in precision is an indicator that *positive* predictions of the classifier are less likely to be correct for some sensitive groups than for others. This may be due to a general lack of training data for some groups, an inherent correlation between sensitive groups and classification difficulty, or a difference in base class prevalence depending on the sensitive group.

The following metrics are only reported in the case of binary classification:
* **Specificity**: A disparity of specificity is an indicator that the classifier tends to produce more false alarms for certains groups of sensitive attributes, which indicates a disparity of performance in distinguishing negative instances.
* **Negative predictive value**: A significant relative or absolute difference in the negative predictive value is an indicator that *negative* predictions of the classifier are less likely to be correct for some sensitive groups than for others. Similar to precision disparity, possible causes are a general lack of training data for some groups, an inherent correlation between sensitive groups and classification difficulty, or a difference in base class prevalence depending on the sensitive group.


Regression
----------

In the context of regression fairness evaluation, we work with continuous target
scores :math:`\bar{R} \in \mathcal{R} = \mathbb{R}` as well as continuous prediction scores
:math:`\hat{R} \in \mathcal{R} = \mathbb{R}`.
We further work with categorical sensitive attributes :math:`A \in \mathcal{A}`
(e.g., gender, race, etc.) with :math:`\mathcal{A} = \{1, \ldots, L\}`.
We distinguish between *Performance Fairness* (parity of prediction performance, i.e., estimation error) and
*Prediction Fairness* (parity of model predictions) which is explained in more detail below.

Performance Fairness
^^^^^^^^^^^^^^^^^^^^

The goal is to determine if the model's prediction performance is equal for all labels within
a sensitive group.

**Mean Absolute Error**: The mean absolute error (MAE) between target and prediction
scores is defined by

.. math::

   \text{MAE}_a = \frac{1}{N_a} \sum^{N_a}_{n=1} | \bar{r}_{n, a} - \hat{r}_{n, a} | ,

where :math:`N_a` is the number of samples where the sensitive attribute is a certain :math:`a \in \mathcal{A}`.
The greater the difference in MAE for different sensitive groups, the more unfair a model is to be considered.

**Point Biserial Correlation**: The point biserial correlation coefficient denotes the correlation
between a categorical binary random variable and a continuous one. It is similar to the Pearson correlation
coefficient but for a categorical and continuous random variable, respectively.
Let :math:`\Delta R = \bar{R} - \hat{R}` denote the estimation error. Since the biserial correlation
coefficient is only defined for binary random variables, we use a "one-vs-all" scheme to compute a
correlation coefficient for each :math:`a \in \mathcal{A}` separately.
Thus, the point biserial correlation coefficient can be calculated by

.. math::

   \rho_{A, \Delta R} = \frac{(\mu_{\Delta R}^{A=a} - \mu_{\Delta R}^{A \neq a})}{\sigma_{\Delta R}}
   \sqrt{\frac{N_{A=a} N_{A \neq a}}{N^2}} ,

where :math:`\mu_{\Delta R}^{A=a}` and :math:`\mu_{\Delta R}^{A \neq a}` denote the mean scores of
the estimation error for all samples with label :math:`{A=a}` and vice versa, whereas
:math:`\sigma_{\Delta R}` denotes the standard deviation of the estimation error.
Furthermore, :math:`N_{A=a}` and :math:`N_{A \neq a}` denote the amount of samples with
label :math:`{A=a}` and vice versa.

**Separation**: This aspect of fairness requires statistical independence between model predictions and
the sensitive attribute given the target scores, so that

.. math::

   \hat{R} \perp A | \bar{R} \rightarrow f(\hat{R}, A | \bar{R}) =  f(\hat{R}| \bar{R})f(A| \bar{R}) .

This metric is sensitive to a possible bias in the target scores itself so that it is useful to solely
quantify the performance of the underlying AI model :cite:p:`fairness-Steinberg2020`.

**Sufficiency**: This aspect of fairness requires statistical independence between target scores and the sensitive
attribute given the predicted scores, so that

.. math::

   \bar{R} \perp A | \hat{R} \rightarrow f(\bar{R}, A | \hat{R}) =  f(\bar{R}| \hat{R})f(A| \hat{R}) .

While **separation** deals with parity of error rates for similar individuals,
sufficency focuses on error parity among individuals who are given the same decision :cite:p:`fairness-Steinberg2020`.
Mathematically, this distinction is similar to the one between precision and recall.

Prediction Fairness
^^^^^^^^^^^^^^^^^^^

In the previous section, we describe the fairness evaluation for the estimation error.
However, it is also possible to quantify the fairness/equality of the model predictions itself.
In case that the underlying data set itself is biased, e.g., towards a certain sensitive attribute,
this will also be reflected by the model predictions if the estimation error is constant for all sensitive groups.
However, this might rather indicate a bias within the data itself instead of a bias within the trained AI model.
Thus, the application of prediction fairness may depend on the use case and what is intended for the current
examination.

*Note*: Since the target is to quantify the fairness of the underlying AI model itself, the following metrics for
*Prediction Fairness* are not considered for the final fairness rating. Currently, only aspects of
*Performance Fairness* are considered for the fairness rating.

**Point Biserial Correlation**: The point biserial correlation coefficient can also be computed for the
model predictions :math:`\hat{R}` itself so that the correlation coefficient is denoted by :math:`\rho_{A, \hat{R}}`.
When the data evaluation of Thetis is active, it will also compute the correlation coefficient between the sensitive
attributes and the target scores :math:`\bar{R}` which yields the correlation coefficient :math:`\rho_{A, \bar{R}}`.
This is useful to determine if a correlation is induced by the data itself or the used AI model.

**Independence**: This aspect requires the equality of predictions for all sensitive attributes which
can be expressed by

.. math::

   \hat{R} \perp A \rightarrow f(\hat{R}, A) =  f(\hat{R})f(A) .


Note that a possible bias in the target values has an influence to the computation of the independence score.
Thus, it is a metric for both, a bias in the target values as well as a bias in the model
prediction performance :cite:p:`fairness-Steinberg2020`.

Object Detection
----------------

The metrics for evaluating the fairness of object detection algorithms are highly related to the ones used
for classification fairness evaluation. However, we have two limitations in the case of object detection:

* In a common object detection setting we do not have access to the *true negatives* (TN, correctly identified background).
* For object predictions with no associated ground-truth information, we commonly do not have information about a sensitive attribute available.

Therefore, only the computation of the ratio/difference of the **recall** (correctly identified objects as such) is
applicable since the FP used in *precision* computation may not contain sensitive attribute information, and the
computation of *specificity* and *negative predictive value* require the presence of TN.


References
----------

.. bibliography::
   :keyprefix: fairness-