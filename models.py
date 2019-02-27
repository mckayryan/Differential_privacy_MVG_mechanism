from model_evaluation import cross_validation_split
from model_evaluation import test_train_split
from model_evaluation import root_mean_squared_error
from tensorflow.keras import metrics
from tensorflow.keras import layers
import tensorflow as tf

# Remove below if with to use GPU
import os
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"   # see issue #152
os.environ["CUDA_VISIBLE_DEVICES"] = '-1'


def keras_seq_reg_model_compilation(features, tf_loss, tf_metrics):

    model_layers = [
        layers.Dense(features, activation='relu', kernel_initializer='normal',
                     kernel_regularizer=tf.keras.regularizers.l2(0.01)),

        layers.Dense(int(features/2), activation='relu',
                     kernel_initializer='normal'),

        layers.Dense(1, kernel_initializer='normal')
    ]

    model = tf.keras.Sequential(model_layers)

    model.compile(optimizer=tf.train.AdamOptimizer(0.001),
                  loss=tf_loss,
                  metrics=tf_metrics)

    return model


def seq_nn_cross_validation(train_data,
                            test_data,
                            folds,
                            X_labels,
                            y_label,
                            fit_params):

    result = list()
    for train_ind, test_ind in cross_validation_split(len(train_data),
                                                      folds=folds):

        train = train_data.iloc[train_ind]
        X_train = train[X_labels].values
        y_train = train[y_label].values

        test = test_data.iloc[test_ind]
        X_test = test[X_labels].values
        y_test = test[y_label].values

        # Create sequential NN model
        model = keras_seq_reg_model_compilation(
            features=X_test.shape[1],
            tf_loss=tf.losses.mean_squared_error,
            tf_metrics=[metrics.mean_squared_error,
                        metrics.kullback_leibler_divergence,
                        metrics.mean_absolute_error])

        # Train model
        model.fit(X_train,
                  y_train,
                  validation_data=(X_test, y_test),
                  **fit_params)

        if 'batch_size' not in fit_params.keys():
            fit_params['batch_size'] = 32

        result += [root_mean_squared_error(
            model.predict(X_test, batch_size=fit_params['batch_size']),
            y_test)]

    return result


def seq_nn_single_evaluation(train_data,
                             test_data,
                             X_labels,
                             y_label,
                             fit_params,
                             test_holdout_p=None,
                             train_ind=None,
                             test_ind=None):

    if train_ind is None or test_ind is None:
        train_ind, test_ind = \
            test_train_split(len(test_data),
                             test_holdout_p)

        train = train_data.iloc[train_ind]
        X_train = train[X_labels].values
        y_train = train[y_label].values
    else:
        X_train = train_data[X_labels].values
        y_train = train_data[y_label].values

    test = test_data.iloc[test_ind]
    X_test = test[X_labels].values
    y_test = test[y_label].values

    # Create sequential NN model
    model = keras_seq_reg_model_compilation(
        features=X_test.shape[1],
        tf_loss=tf.losses.mean_squared_error,
        tf_metrics=[metrics.mean_squared_error,
                    metrics.kullback_leibler_divergence,
                    metrics.mean_absolute_error])

    # Train model
    model.fit(X_train,
              y_train,
              # validation_data=(X_test, y_test),
              **fit_params)

    if 'batch_size' not in fit_params.keys():
        fit_params['batch_size'] = 32

    result = root_mean_squared_error(
        model.predict(X_test, batch_size=fit_params['batch_size']),
        y_test)

    return result
