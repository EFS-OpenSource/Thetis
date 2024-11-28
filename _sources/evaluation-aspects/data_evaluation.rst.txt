.. _Data quality:

Data quality
============

The computation of system quality attributes greatly depends on the quality and quantity of available evaluation data.
Therefore, Thetis offers a comprehensive assessment and rating of the evaluation dataset used. This assessment and rating
are tailored to the selected application task.

Classification
--------------

For a classification dataset with :math:`N` samples and :math:`K` classes, Thetis evaluates the ratio between the
different class labels. The more the label distribution approximates a uniform distribution, the higher the rating for the
dataset. In the future, we seek to enable Thetis to also evaluate further aspects such as diversity and data quality.

Regression
----------

Similar to the evaluation of dataset quality in the context of classification, we consider a uniform distribution
to be the optimal ground truth data distribution for training/evaluation data in order to avoid a potential bias during
training and evaluation. Thus, dataset quality is evaluated according to the uniformity of the sample distribution.

Additionally, the quality of fairness-related features is also included in the assessment of dataset quality
(see classification function for more details). In this context, the point biserial correlation coefficient between
the sensitive attribute and the target scores is computed in order to examine the dataset for a possible bias towards a
certain feature (see documentation of fairness package for more details about point biserial correlation).

Object detection
----------------

In contrast to classification, the ratio between different labels is neglected for dataset rating, since an object
detector might also be designed to only work with a single class. Instead, it is evaluated how "distributed" or spread
the real (ground truth) objects are over the available image space. A dataset with equally distributed object locations
over the entire image space will receive a higher rating.
