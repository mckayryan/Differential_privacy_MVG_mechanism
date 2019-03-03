import numpy


def root_mean_squared_error(y_true, y_pred, divisor=None):
    '''
    Computation of evaluation metric Root Mean Squared Error
    Implementation can handle large inputs using 'divisor'
    '''
    res = list()
    length = len(y_pred)
    if divisor is not None and length % divisor == 0:
        for i in range(length/divisor):
            res += [numpy.sum(
                pow(
                    numpy.subtract(y_true[i*divisor:(i+1)*divisor],
                                   y_pred[i*divisor:(i+1)*divisor]),
                    2)) /
                    float(len(y_true))]
    else:
        res = [numpy.sum(
            pow(
                numpy.subtract(y_true,
                               y_pred),
                2)) /
               float(len(y_true))]
    return pow(numpy.sum(res), 0.5)


def mean_absolute_error(y_true, y_pred, divisor=None):
    '''
    Computation of evaluation metric Mean Absolute Error
    Implementation can handle large inputs using 'divisor'
    '''
    res = list()
    length = len(y_pred)
    if divisor is not None and length % divisor == 0:
        for i in range(length/divisor):
            res += [numpy.sum(
                abs(numpy.subtract(y_true[i*divisor:(i+1)*divisor],
                                   y_pred[i*divisor:(i+1)*divisor]))
            ) / float(len(y_true))]
    else:
        res = [numpy.sum(
            abs(numpy.subtract(y_true,
                               y_pred))
        ) / float(len(y_true))]
    return numpy.sum(res)


# Metric for Covariance estimation:
# Residual Sum Squares of 'total variance captured'
def principle_component_RSS(true, pred):
    true_eigenvals, _ = numpy.linalg.eig(true)
    pred_eigenvals, _ = numpy.linalg.eig(pred)
    return numpy.sum(pow(numpy.subtract(true_eigenvals, pred_eigenvals), 2))
