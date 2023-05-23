.. _Fairness:

Fairness
========

The evaluation of fairness of an AI algorithm is highly important to assess for a possible discrimination of
individual sensitive groups. Thetis evaluates for *group fairness* which evaluates the risk for individual groups of
experiencing discrimination. The fairness rating of an AI model is based on several fairness metrics which are
described in the following.

Classification
--------------

**Demographic Parity Difference:** the Demographic Parity states that the decisions of an AI algorithm are independent
of a certain feature which describes a sensitive group (e.g., the predictions are independent of feature *gender*)
:cite:p:`fairness-Agarwal2018`.
Given an input :math:`X \in \mathcal{X}`, a classification model :math:`h(X)` makes predictions
:math:`\hat{Y} \in \mathcal{Y}` targeting the ground-truth label :math:`\bar{Y} \in \mathcal{Y}`, so that
:math:`h: \mathcal{X} \rightarrow \mathcal{Y}`. Furthermore, let :math:`A \in \mathcal{A}` denote a sensitive feature
(e.g., attribute *gender*) for each :math:`X`. Demographic parity is reached if the prediction :math:`h(X)` is
statistically independent of :math:`A`, so that

.. math::

   \mathrm{E}_{X}\Big[ h(X) | A = a \Big] = \mathrm{E}_{X}\Big[ h(X) \Big], \quad \forall a \in \mathcal{A} ,

is fullfilled :cite:p:`fairness-Agarwal2018`.

The *Demographic Parity Difference* is now defined as the difference between the smallest and the largest selection
rate (expectation of model predictions w.r.t. the sensitive feature), so that is can be obtained by

.. math::

   \max_{a \in \mathcal{A}} \mathrm{E}_{X}\Big[ h(X) | A = a \Big] -
   \min_{a \in \mathcal{A}} \mathrm{E}_{X}\Big[ h(X) | A = a \Big] .


**Equalized Odds Difference:** the aim of the equalized odds fairness metric is to make sure that a machine learning
model works equally well for various groups. It is stricter than demographic parity because it not only demands
that the model's predictions are not influenced by sensitive group membership but also requires that the groups
have the same rates of false positive and true positive predictions :cite:p:`fairness-Agarwal2018`.
More formally, it equalized odds can be described by

.. math::

   \mathrm{E}_{X}\Big[ h(X) | A = a, \bar{Y} = \bar{y} \Big] = \mathrm{E}_{X}\Big[ h(X) | \bar{Y} = \bar{y} \Big],
   \quad \forall a \in \mathcal{A}, \bar{y} \in \mathcal{Y} .


This difference is significant because a model may achieve demographic parity but it could
still produce more false positive predictions for one group compared to others :cite:p:`fairness-Agarwal2018`.

The *Equalized Odds Difference* reflects the greater of either *true positive rate difference* or
*false positive rate difference* metrics. Both metrics are computed in a similar way as the *Demographic Parity
Difference* and denote the difference between largest and smallest score of true/false positive rate scores across
the sensitive groups.

Regression
----------

Coming soon.

Object Detection
----------------

The metrics for evaluating the fairness of object detection algorithms are highly related to the ones used
for classification fairness evaluation. However, the computation of the *Equalized Odds Difference* is not directly
applicable since it is also based on the *false positive rate* which, in turn, needs access to the *true negatives*,
i.e., correctly identified background.

Therefore, we use the **Demographic Parity Difference** metric to evaluate the fairness of object detections on
a dedicated evaluation data set.

References
----------

.. bibliography::
   :keyprefix: fairness-