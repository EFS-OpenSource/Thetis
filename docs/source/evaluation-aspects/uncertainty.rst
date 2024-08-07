.. _Uncertainty:

Uncertainty consistency (calibration)
=====================================

AI models typically make decisions for each input, regardless of their level of uncertainty. In safety-critical
scenarios, it is crucial for the model to provide a reliable self-assessment of its uncertainty. This allows for
appropriate fallback solutions to be applied when the model is unsure of its decision.

Thetis analyzes and evaluates the quality and consistency of the uncertainty that is estimated and attached to each
AI prediction in most cases (e.g., score or confidence information in classification, "objectness" score in object
detection, or variance estimation in probabilistic regression settings).
The evaluation of uncertainty quality depends on the selected task. We give a brief overview about the mathematical
background and the used metrics in the following section.

Classification
--------------

Given an input :math:`X \in \mathcal{X}`, an AI model predicts a label :math:`\hat{Y} \in \mathcal{Y}` targeting
the ground truth label :math:`\bar{Y} \in \mathcal{Y}`.
For binary classification, the set of labels is :math:`\mathcal{Y} \in \{0, 1\}` and the AI model commonly outputs
a (probability) score :math:`\hat{P} \in [0, 1]`, denoting the confidence in predicting the positive class.
The uncertainty estimation of a binary classification model is *well calibrated*, if

.. math::

   \mathbb{P}(\bar{Y} = 1 | \hat{P} = \hat{p}) = \hat{p}, \quad \forall \hat{p} \in [0, 1] ,

is fulfilled :cite:p:`uncertainty-Naeini2015`, :cite:p:`uncertainty-Guo2018`, :cite:p:`uncertainty-Kueppers2023`. For example, consider 100 predictions of an AI model,
each one with a confidence score of 80%. If we observe an accuracy of 80% as well, the AI model is *well-calibrated*.

In multi-class classification settings (:math:`\mathcal{Y} \in \{1, \ldots, K\}` with :math:`K` classes), the
definition for uncertainty calibration is similar to the binary classification case by

.. math::

   \mathbb{P}(\hat{Y} = \bar{Y} | \hat{P} = \hat{p}) = \hat{p}, \quad \forall \hat{p} \in [0, 1] .

Measuring calibration can be done using several metrics:

**Expected Calibration Error (ECE):** the ECE can be derived from the definition for calibrated classification
uncertainty and is a common metric to measure miscalibration :cite:p:`uncertainty-Naeini2015`. The target is to measure the
expectation of the difference between predicted confidence and observed accuracy :cite:p:`uncertainty-Naeini2015`,
:cite:p:`uncertainty-Guo2018`, :cite:p:`uncertainty-Kueppers2023`, which is denoted by

.. math::

   \mathbb{E}_{\hat{P} \sim f_{\hat{P}}} \Big[ | \mathbb{P}(\hat{Y} = \bar{Y} | \hat{P} = \hat{p}) - \hat{p} | \Big].

Since the expectation is given over a continuous distribution, it is directly tractable.
Instead, the ECE is an approximation of the expectation by applying a binning scheme over the confidence space.
Each predicted sample is grouped into a bin by its confidence. Afterwards, we can compare the average accuracy with
the average confidence within each bin to compute the *conditional* probability of correctness.
Thus, the ECE is given by

.. math::

   \text{ECE} := \sum^{B}_{b=1} \frac{N_b}{N} | \text{acc}(b) - \text{conf}(b) | ,

with :math:`B` bins, :math:`N` samples within the evaluation dataset, :math:`N_b` samples within a single bin, and with
:math:`\text{acc}(b)` and :math:`\text{conf}(b)` as the accuracy and average confidence within bin :math:`b`, respectively.

**Maximum Calibration Error (MCE):** the MCE is highly related to the ECE but denotes the *maximum* difference
between average confidence and accuracy over the binning scheme :cite:p:`uncertainty-Naeini2015`. Thus, the MCE is given by

.. math::

   \text{MCE} := \max_{b \in \{1, \ldots, B\}} | \text{acc}(b) - \text{conf}(b) | .

**Negative Log Likelihood (NLL):** the NLL can be interpreted as a proper scoring rule that estimates the deviation
between a predicted probability distribution and the true distribution. Thus, the NLL function is also commonly
used as a complementary uncertainty metric.

**Brier Score:** similar to the NLL, the Brier Score is also a proper scoring rule and is given by the
mean squared error of the forecast. It is also commonly used as a complementary calibration metric.

**Homogeneity Rating:** one of the rating aspects is the homogeneity of the calibration error. Thetis assigns a
higher rating if the calibration error is constant across the different levels of confidence, i.e., when the
variance of the calibration error for different confidence levels is low.

**Outlier Rating:** a further rating aspect is the presence/absence of confidence intervals with a significantly
higher calibration error compared to the average level of miscalibration.

Regression (probabilistic)
--------------------------

In the context of regression (estimation of a continuous target score), several machine learning/deep learning
algorithms are able to output an estimation uncertainty along with the predicted score.
Similar to the classification case, this uncertainty shall reflect the (expected) prediction error. If the AI
model consistently over- or underestimates the prediction error, it is considered to be *miscalibrated*.

Mathematically, a (probabilistic) AI model takes an (arbitrary) input and predicts a
mean :math:`\mu_\hat{R} \in \mathbb{R}` and variance :math:`\sigma^2_\hat{R} \in \mathbb{R}_{>0}`,
so that the random variable for the model predictions is given by
:math:`\hat{R} \sim \mathcal{N}(\mu_\hat{R}, \sigma^2_\hat{R})`, targeting the ground truth
score :math:`\bar{R} \in \mathbb{R}`.

There exist several definitions for the term uncertainty calibration in the context of
probabilistic regression :cite:p:`uncertainty-Kueppers2022b`. The commonly used definition is
*quantile calibration* where it is required that the estimated prediction intervals for a certain quantile level
:math:`\tau \in (0, 1)` cover :math:`\tau%` of the ground truth scores of a validation dataset.

More formally, let :math:`\hat{F}_{\hat{R}}: \mathbb{R} \rightarrow (0, 1)` be the predicted
cumulative distribution function (CDF) of :math:`\hat{R}` and the (inverse) percent point
function (PPF), i.e., the quantile function be given by
:math:`\hat{F}_{\hat{R}}^{-1}: (0, 1) \rightarrow \mathbb{R}` accordingly.
A prediction model is quantile calibrated, if

.. math::

   \mathbb{P} \Big( \bar{R} \leq \hat{F}_{\hat{R}}^{-1}(\tau) \Big) = \tau, \quad \forall \tau \in (0, 1) ,

is fulfilled.

Several metrics exist to evaluate for *quantile calibration*:

**Quantile loss aka Pinball loss**:

.. math::

   \mathcal{L}_{\text{Pin}}(\tau) =
   \begin{cases}
       (\bar{r} - \hat{F}_{\hat{R}}^{-1}(\tau))\tau \quad &\text{if } \bar{r} \geq \hat{F}_{\hat{R}}^{-1}(\tau) \\
       (\hat{F}_{\hat{R}}^{-1}(\tau) - \bar{r})(1 - \tau) \quad &\text{if } \bar{r} < \hat{F}_{\hat{R}}^{-1}(\tau)
   \end{cases}

**Quantile Calibration Error**:
The quantile calibration error measures the absolute difference between expected quantile level and actual quantile
coverage of the ground truth scores by the predicted distributions for a certain quantile level
:cite:p:`uncertainty-Kueppers2022b`. For a dataset with :math:`N` samples, the QCE is given by

.. math::

   QCE(\tau) := \Bigg| \frac{1}{N} \sum^N_{n=1} \mathbb{1}(\epsilon_{\bar{R}_n} \leq \chi^2(\tau)) - \tau \Bigg| ,

where :math:`\chi^2(\tau)` denotes the PPF of the Chi-Square distribution with 1 degree of freedom.
Furthermore, :math:`\epsilon_{\bar{R}_n}` denotes the Normalized Estimation Error Squared (NEES),
also known as the squared Mahalanobis distance, which is given for the one-dimensional case by

.. math::

   \epsilon_{\bar{R}_n} :=  \frac{(\bar{R} - \mu_{\hat{R}})^2}{\sigma^2_{\hat{R}}} .

**Proper scoring rules: Negative Log Likelihood (NLL)**:
The NLL for continuous random variables is given by

.. math::

   NLL := - \frac{1}{N} \sum^N_{n=1} \log \Big(f_{\hat{R}}(\bar{r}; \mu_{\hat{R}}, \sigma^2_{\hat{R}})\Big) ,

with :math:`f_{\hat{R}}(\bar{r}; \mu_{\hat{R}}, \sigma^2_{\hat{R}})` as the probability density function (PDF)
of the predicted distribution at ground truth score :math:`\bar{r}`.
The NLL can be used as a metric to evaluate the uncertainty calibration properties of an estimator since
it captures the goodness of fit of probability distributions. It jointly measures the baseline
prediction performance as well as the quality of the uncertainty estimates.

Object detection
----------------

In contrast to classification, the task of (image-based) object detection is to estimate the presence and location
of multiple objects within a single image. Thus, object detection is the joint task of (semantic) classification and
(spatial) regression.

For the uncertainty calibration evaluation of the **semantic classification** output (e.g., objectness score), we can
use the same metrics as for the standard classification uncertainty calibration evaluation.
The uncertainty evaluation differs from standard classification evaluation in two ways:

1. Since most applications do not have access to the *true negatives* (correctly identified background as such), it is
   not possible to calculate the accuracy. Thus, the calibration target is the precision :cite:p:`uncertainty-Kueppers2020`.
2. For the computation of the precision, it is necessary to match predicted objects with real existing (ground truth)
   objects. However, this matching strategy depends on the selected Intersection over Union (IoU) score. The specified
   IoU describes to which degree predicted and existing objects need to overlap to be considered as matching. Thus,
   all evaluation results are given w.r.t. a certain IoU score.

Furthermore, recent work has shown that the calibration error might also be position-dependent
:cite:p:`uncertainty-Kueppers2020`, :cite:p:`uncertainty-Kueppers2022a`, i.e., the calibration properties of objects located in the center
of an image might differ from objects located at the image boundaries.
Thus, given an object detection model that estimates an object with label :math:`\hat{Y} \in \mathcal{Y}`,
confidence :math:`\hat{P} \in [0, 1]`, and position information :math:`\hat{\mathbf{R}} \in \mathcal{R}`,
*position-dependent* calibration is defined by

.. math::

   \mathbb{P}(\hat{M} = 1 | \hat{P} = \hat{p}, \hat{Y} = \hat{y}, \hat{\mathbf{R}} = \hat{\mathbf{r}}) = \hat{p}, \\
   \forall \hat{p} \in [0, 1], \hat{y} \in \mathcal{Y}, \hat{\mathbf{r}} \in \mathcal{R} ,

where :math:`\hat{M}` evaluates to :math:`1` if the predicted object matches a real existing (ground truth) object.

**Detection Expected Calibration Error (D-ECE):** from this definition, we can derive the D-ECE similar as to the ECE.
The target is to minimize the position-dependent expectation of the difference between predicted
confidence and observed precision. The D-ECE is an approximation by applying a multi-dimensional binning scheme over
the joint confidence, label, and position space :cite:p:`uncertainty-Kueppers2020`, :cite:p:`uncertainty-Kueppers2022a`, and is given by

.. math::

   \text{D-ECE} := \sum^{B}_{b=1} \frac{N_b}{N} | \text{prec}(b) - \text{conf}(b) | ,

with :math:`B` bins, :math:`N` samples within the evaluation dataset, :math:`N_b` samples within a single bin, and with
:math:`\text{prec}(b)` and :math:`\text{conf}(b)` as the precision and average confidence within bin :math:`b`, respectively.

For the uncertainty calibration evaluation of the **spatial regression** output (uncertainty for bounding box position),
we simply adapt the methods used for uncertainty calibration evaluation in the context of (probabilistic)
regression :cite:p:`uncertainty-Kueppers2022b`, :cite:p:`uncertainty-Kueppers2023`.

Similar to the evaluation of classification uncertainty, Thetis also applies a rating for **Homogeneity** and
**Outliers** in the context of object detection uncertainty evaluation.

References
----------

.. bibliography::
   :keyprefix: uncertainty-