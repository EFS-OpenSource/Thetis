Preparing input data
====================

The Thetis evaluation library only requires the output of an AI model on a dedicated evaluation dataset.
Thus, the application requires the ground truth target labels (not the data itself!) and the according AI predictions.
We give a detailed overview about the required data format in the following.

Binary classification
---------------------
In the case of binary classification, Thetis expects two instances of a `Pandas DataFrame <https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html>`__ :code:`pd.DataFrame`
representing the annotations and the model predictions on the dataset, respectively.

Imagine that we have the variables :code:`annotations` and :code:`predictions` with annotations and predictions, respectively.
If we print the content of :code:`annotations` to the Python console, it might output the following:

.. code-block:: python

   >>> annotations
              target  gender    age
   img_00     person  female  adult
   img_01     person    male  child
   img_02     person  female  adult
   img_03     person  female  adult
   img_04     person  female  adult
   img_05     person  female  adult
   img_06  no person    male  adult
   img_07  no person  female  adult
   img_08     person  female  child
   img_09     person  female  child

In this example, we have the available target classes "person" and "not person" with the sensitive
attributes "gender" and "age". The target labels must always be given in the column :code:`target`. Furthermore,
each sensitive attribute must be given with its respective name as column name.

Accordingly, the output of :code:`predictions` might look like the following:

.. code-block:: python

   >>> predictions
              labels  confidence
   img_00     person    0.992300
   img_01     person    0.962620
   img_02  no person    0.146000
   img_03     person    0.795490
   img_04     person    0.897310
   img_05  no person    0.247210
   img_06  no person    0.001412
   img_07  no person    0.000150
   img_08     person    0.970410
   img_09     person    0.931941

The required column :code:`labels` holds the predicted label for each item in the dataset, whereas the required
column :code:`confidence` represents the (binary) label confidence/uncertainty estimated by the AI model.

**Important:** the :code:`confidence` refers to the :code:`binary_positive_label` specified in the `application config <#>`__.
The uncertainty for the negative class ("no person" in this case) is given by :code:`1 - confidence`.

**Note:** the indices of the DataFrames :code:`annotations` and :code:`predictions` must match to each other.

Multi-class classification
--------------------------

If you are working in a multi-class classification setting (setting "task" to "classification" with more than 2 entries
in "distinct_classes" in the `application config <#>`__), Thetis also expects two Pandas DataFrames :code:`annotations`
and :code:`predictions` representing the ground truth annotations and the according AI predictions, respectively.

Similar to the binary classification case, the DataFrame :code:`annotations` must consist of the columns :code:`target`
as well as an own column for each specified sensitive attribute:

.. code-block:: python

   >>> annotations
            target  gender    age
   img_00   person  female  adult
   img_01   person    male  child
   img_02      car    None   None
   img_03  bicycle    None   None
   img_04      car    None   None
   img_05   person  female  child
   img_06      car    None   None
   img_07   person  female  adult
   img_08   person    male  adult
   img_09  bicycle    None   None

**Note:** in this example, the sensitive attributes "gender" and "age" are only valid for the target class "person".
This must be specified in the `fairness section of the application config <#>`__. For all other entries, the
missing entries are marked by passing "None".

The respective AI predictions given by :code:`predictions` are given in a similar way compared to binary classification.
A column :code:`labels` is required, representing the predicted label of each individual sample.
However, an uncertainty/confidence is required for each possible class (e.g., the output of a Softmax activation function
in the context of neural networks). The columns for the confidence must follow the naming convention
:code:`confidence_<label>`. Thus, given a configuration for "distinct_classes" with possible classes "person",
"bicycle", and "car", the DataFrame :code:`predictions` for the AI predictions might look like the following:

.. code-block:: python

   >>> predictions
            labels  confidence_person  confidence_bicycle  confidence_car
   img_00   person           0.984100            0.014250        0.001650
   img_01   person           0.948210            0.035340        0.016450
   img_02      car           0.001020            0.021920        0.977060
   img_03      car           0.021412            0.420190        0.558398
   img_04      car           0.030120            0.001390        0.968490
   img_05  bicycle           0.361530            0.591312        0.047158
   img_06      car           0.000326            0.005310        0.994364
   img_07   person           0.873920            0.004124        0.121956
   img_08   person           0.968320            0.020931        0.010749
   img_09   biycle           0.015182            0.947182        0.037636

**Note:** the indices of the DataFrames :code:`annotations` and :code:`predictions` must match to each other.

Regression
----------

In the case of regression, Thetis expects two instances of a `Pandas DataFrame <https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html>`__ :code:`pd.DataFrame`
representing the annotations (target scores) and the model predictions on the dataset, respectively.

Imagine that we have the variables :code:`annotations` and :code:`predictions` with annotations and predictions, respectively.
If we print the content of :code:`annotations` to the Python console, it might output the following:

.. code-block:: python

   >>> annotations
               target  gender    age
   sample_00   -1.246  female  adult
   sample_01    0.579    male  child
   sample_02    0.000  female  adult
   sample_03  -10.798  female  adult
   sample_04    3.480  female  adult
   sample_05    9.546  female  adult
   sample_06   70.892    male  adult
   sample_07  -16.721  female  adult
   sample_08    0.239  female  child
   sample_09   -0.724  female  child

In this example, we have the target scores with the sensitive
attributes "gender" and "age". The target labels must always be given in the column :code:`target`. Furthermore,
each sensitive attribute must be given with its respective name as column name.

Accordingly, the output of :code:`predictions` might look like the following:

.. code-block:: python

   >>> predictions
             predictions  stddev
   sample_00     -0.524    1.272
   sample_01      2.725    0.713
   sample_02      0.011    0.005
   sample_03     -8.372    2.795
   sample_04     -2.745    3.657
   sample_05      9.546    0.001
   sample_06     60.126    9.001
   sample_07     -3.913    4.503
   sample_08     -0.342    0.098
   sample_09     -0.223    0.003

The required column :code:`predictions` holds the predicted scores for each item in the dataset. The *optional* column
:code:`stddev` holds the *estimated* standard deviation for each predicted score representing the estimation
uncertainty. Alternatively, the column :code:`variance` can also be passed with the according estimation variance.

**Note:** when the evaluation of uncertainty is active, either column :code:`stddev` or :code:`variance` must be given.

**Note:** the indices of the DataFrames :code:`annotations` and :code:`predictions` must match to each other.

Object detection
----------------

The input for the image-based object detection evaluation case differs compared to the classification cases.
In the object detection evaluation mode, Thetis expects two Python dictionaries :code:`annotations` and
:code:`predictions`, representing the ground truth objects as well as the predicted objects, respectively.

Each entry within these dictionaries must be an instance of a `Pandas DataFrame <https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html>`__.
The dictionary keys are the identifiers for each image. Thus, it is possible to assign predicted objects to real
existing ones by identifying the ground truth and prediction information using the given dictionary keys.

The individual :code:`pd.DataFrame` instances (annotations and predictions) for each frame must be given according
to the format for `binary classification <Binary Classification>`_ (but with more than 2 labels allowed). Thus, the
console output for :code:`annotations` might look like the following:

.. code-block:: python

   >>> annotations
   {'__meta__':
               width   height
       img_00   1920     1080
       img_01   1680     720,

    'img_00':
            target  gender    age
        0   person  female  adult
        1   person    male  child
        2      car    None   None
        3   person  female  child
        4      car    None   None
        5   person  female  adult,
   'img_01': ...
   }

**Important:** the dictionary for :code:`annotations` *requires* a field :code:`__meta__` with an instance of
:code:`pd.DataFrame` with columns :code:`width` and :code:`height`. This DataFrame holds the width and height meta
information for the respective image. The frame index must match the set of keys that are present in
:code:`annotations` and :code:`predictions`.

The console output for :code:`predictions` might look like:

.. code-block:: python

   >>> predictions
   {'img_00':
           labels  confidence
       0   person    0.914123
       1   person    0.871923
       2      car    0.921751
       3      car    0.993720
       4      car    0.351152
       5  bicycle    0.639153
       6      car    0.817591
       7   person    0.912730
       8   person    0.981693
       9   biycle    0.583190,
   'img_01': ...
   }

**Note:** the indices of the individual :code:`pd.DataFrame` instances are not expected to match each other since
the amount of predicted and real-existing objects can differ.

Furthermore, only a single field for :code:`confidence` is expected, even when working with multiple labels.
This is because most of the common object dection algorithms only output a single confidence estimate for a detected
object, discarding the confidence information for the remaining classes.

