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

Coming soon.

Object Detection
----------------

In contrast to classification, the ratio between different labels is neglected for data set rating, since an object
detector might also be designed to only work with a single class. Instead, it is evaluated how "distributed" or spread
the real (ground-truth) objects are over the available image space. A data set with equally distributed object
locations over the whole image space will get a higher rating.
