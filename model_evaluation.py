import numpy
import random
import pandas


# Metric for Covariance estimation:
# Residual Sum Squares of 'total variance captured'
def principle_component_RSS(true, pred):
    true_eigenvals, _ = numpy.linalg.eig(true)
    pred_eigenvals, _ = numpy.linalg.eig(pred)
    return numpy.sum(pow(numpy.subtract(true_eigenvals, pred_eigenvals), 2))


def root_mean_squared_error(y_true, y_pred):
    '''
    Computation of evaluation metric RMSE
    '''
    return pow(
        numpy.sum(pow(
            numpy.subtract(y_pred, y_true), 2))
        / len(y_true),
        0.5)


def test_train_split(y_len, test_perc):
    if test_perc >= 0.0 and test_perc <= 1.0:
        selection_pool = range(y_len)
        test_size = int(y_len * (1.0 - test_perc))

        selected = [
            selection_pool.pop(random.randrange(len(selection_pool)))
            for _ in xrange(test_size)
        ]

        return selected, selection_pool
    else:
        print('test_train_split_indicies: \tparameter "test_perc" must have ')
        print('\t\t\t\tvalue between 0 and 1, not {p}'.format(p=test_perc))


def cross_validation_split(y_len, folds):
    if not(isinstance(folds, int)):
        print('cross_validation: \tparameter "folds" must be integer')
    else:
        selection_pool = range(y_len)
        test_size = int(y_len * (1.0 / folds))

        for _ in xrange(folds):
            selected = [
                selection_pool.pop(random.randrange(len(selection_pool)))
                for _ in xrange(test_size)
            ]

            yield selected, [i for i in xrange(y_len) if i not in selected]


def record_result(results, column_names, new_data):
    if results is None:
        new = pandas.DataFrame(new_data, columns=column_names)

    else:
        new = pandas.concat([
            results,
            pandas.DataFrame(new_data, columns=column_names)
        ])
    return new
