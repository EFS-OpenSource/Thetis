.. _Data Quality:

Data Quality
============

The computation of safety-relevant metrics highly depends on the quality and amount of available evaluation data.
Thus, Thetis provides a complementary assessment and rating of the used evaluation data set. The assessment and rating
depends on the selected application task.

Classification
--------------

For a classification data set with :math:`N` samples and :math:`K` classes, Thetis evaluates the ratio between the
different class labels. The more the label distribution equals a uniform distribution, the higher the rating for the
data set. In the future, we seek to enable Thetis to also evaluate further aspects such as diversity and data quality.

Regression
----------

Similar to the evaluation of data set quality in the context of classification, we consider a uniform distribution
to be the optimal ground truth data distribution for training/evaluation data in order to avoid a potential bias during
training and evaluation. Thus, data set quality is evaluated according to the uniformity of the sample distribution.

Additionally, the quality of fairness-related features is also included in the assessment of data set quality
(see classification function for more details). In this context, the point biserial correlation coefficient between
the sensitive attribute and the target scores is computed in order to examine the data set for a possible bias towards a
certain feature (see documentation of fairness package for more details about point biserial correlation).

Object Detection
----------------

In contrast to classification, the ratio between different labels is neglected for data set rating, since an object
detector might also be designed to only work with a single class. Instead, it is evaluated how "distributed" or spread
the real (ground truth) objects are over the available image space. A data set with equally distributed object
locations over the whole image space will get a higher rating.
