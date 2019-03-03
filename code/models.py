from tensorflow.keras import metrics
from tensorflow.keras import layers
import tensorflow as tf

from numpy.random import uniform
import pandas
import numpy

# Local imports
from thundersvmScikit import SVR

from model_evaluation import cross_validation_split
from model_evaluation import test_train_split

from metrics import root_mean_squared_error

# Remove below if with to use GPU
# import os
# os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"   # see issue #152
# os.environ["CUDA_VISIBLE_DEVICES"] = '-1'


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


def svr_parameter_tuning(X,
                         y,
                         scoring_function,
                         rand_iters=100,
                         search_range=(0.001, 3),
                         holdout_split=0.2,
                         kernel='rbf',
                         privacy_mechanism_sampler=None,
                         privacy_mechanism_params=None,
                         privacy_sample_iterations=5):

    import operator

    # Randomised parameter search
    param_selections = dict()

    for i in range(rand_iters):

        train_ind, test_ind = test_train_split(y_len=len(y),
                                               test_perc=holdout_split)

        if (privacy_mechanism_sampler is not None
                and privacy_mechanism_params is not None):
            #           Sample periodically for efficiency
            if i % privacy_sample_iterations == 0:
                sample = privacy_mechanism_sampler(
                    pandas.DataFrame(
                        numpy.append(X[train_ind],
                                     y[train_ind],
                                     axis=1)),
                    **privacy_mechanism_params)
                train_X = sample.values[:, :-1]
                train_y = sample.values[:, -1]
        else:
            train_X = X[train_ind]
            train_y = y[train_ind]

        c = round(uniform(search_range[0], search_range[1]), 4)
        g = round(uniform(search_range[0], search_range[1]), 4)

        model = SVR(kernel=kernel, C=c, gamma=g)
        model.fit(train_X, train_y)

        param_selections[(c, g)] = \
            scoring_function(
                y[test_ind],
                model.predict(X[test_ind]).reshape(-1, 1),
                100)

    best_C, best_gamma = \
        min(param_selections.items(), key=operator.itemgetter(1))[0]

    return dict(
        best_C=best_C,
        best_gamma=best_gamma,
        best_rmse=min(param_selections.values()),
        results=param_selections)


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
