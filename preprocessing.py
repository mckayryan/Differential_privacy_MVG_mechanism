import numpy
import pandas


def centre_data(data):
    return data - data.mean()


def scale_data(data, target_bounds, data_bounds=None):
    '''
       Requires:
           data           - Pandas DataFrame floats
           bounds         - Dictionary: Upper and lower bounds for
                            labelled columns in 'data'
           target_scale   - Tuple: Upper and lower bounds for scaled 'data'
           centre_data    - Bool: Flag to indicate if data should be centred
                            before scaling

       Returns:
           result         - Pandas DataFrame with "data" columns
                            scaled to "target_scale"
    '''
    if isinstance(target_bounds, tuple):
        min_target, max_target = target_bounds

    result = data.copy()

    if data_bounds is None:
        data_bounds = dict()
        for key in list(data.columns.values):
            data_bounds[key] = (data[key].min(), data[key].max())

    for key in list(data.columns.values):
        if key in data_bounds.keys():
            min_data, max_data = data_bounds[key]
            if isinstance(target_bounds, dict):
                min_target, max_target = target_bounds[key]
            result[key] = (data[key]
                           .apply(lambda x:
                                  min_target +
                                  ((max_target - min_target) *
                                   (float(x) - min_data)) /
                                  (max_data - min_data)
                                  ))
        else:
            print('Warning: scale_data: column "{c}" \
                   is not present in data with columns: \n{col}'.format(
                c=key, col=list(data.columns.values)))

    return result


def centered_sample_covariance_matrix(X):
    '''
        Requires
            X        - dataset

        Returns      - zero mean covariance estimation query
    '''
    if isinstance(X, pandas.core.frame.DataFrame):
        result = pow(X.shape[0], -1)*numpy.transpose(X).dot(X)
    else:
        result = pow(X.shape[0], -1)*numpy.matmul(numpy.transpose(X), X)
    return result


def rescale_feature(feature,
                    original_bound,
                    update_bound,
                    current_bound,
                    target_bound):
    min_o, max_o = original_bound
    min_c, max_c = current_bound
    min_u, max_u = update_bound
    min_t, max_t = target_bound
    original_scale = min_o + ((feature - min_c) *
                              (max_o - min_o) /
                              (max_c - min_c))
    return min_t + (max_t - min_t) * (original_scale - min_u) / (max_u - min_u)
