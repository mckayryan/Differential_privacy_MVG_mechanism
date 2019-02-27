import numpy

# Establish parameters: gaussian_sensitivity, MVG_sensitivity


def centered_covariance_query_sensitivity(n, m, c):
    '''
       'A Differential Privacy Mechanism Design Under Matrix-Valued Query'
        Chanyaswad, Dytso, Poor & Mittal 2018, p.18.:
        https://arxiv.org/abs/1802.10077 (accessed 16/12/2018) [1]

       Requires
           n   - divisor of query function
           m   - number of unit values / observations to be varied
                 under adjacency definition
           c   - maximum possible value in range of single observation

       Returns - Sensitivity calculation for zero mean
                 covariance estimation query
                 ie f(X) = n^-1 * transpose(X)X
    '''
    return (2 * float(m) * float(c)**2) / float(n)


'''
    Examples:
        get_query_point_sensitivity(query_type='identity',
                                    query_scale=feature_scale,
                                    query_shape=(train_size,features)
        get_query_point_sensitivity(query_type='covariance',
                                    query_scale=feature_scale,
                                    query_shape=(train_size,features)
'''


def get_query_point_sensitivity(query_scale, query_shape, query_type):
    if query_type == 'identity':
        # Global maximum of change for any
        # single point change in query f(X) = X
        result = abs(numpy.subtract(query_scale[0], query_scale[1]))
    elif query_type == 'covariance':
        # Global maximum of change for a single point
        # change in query f(X) = (1/n)*transpose(X)X
        result = centered_covariance_query_sensitivity(n=query_shape[0],
                                                       m=1.0,
                                                       c=query_scale[1])
    else:
        print("get_query_point_sensitivity: \
        required query_type in ('identity','covariance')")
        result = None
    return result


'''
    Examples:
        get_query_row_sensitivity(query_type='identity',
                                  query_scale=feature_scale,
                                  query_shape=(train_size,features))
        get_query_row_sensitivity(query_type='covariance',
                                  query_scale=feature_scale,
                                  query_shape=(train_size,features))
'''


def get_query_row_sensitivity(query_scale, query_shape, query_type):
    if query_type == 'identity':
        # Global maximum of change for any data row / observation
        # change in query f(X) = X
        # Section 8.1.3 p30 of paper [1]
        sensitivity = get_query_point_sensitivity(query_scale,
                                                  query_shape,
                                                  'identity')
        result = pow(query_shape[1] * pow(sensitivity, 2),
                     0.5)
    elif query_type == 'covariance':
        # Global maximum of change for any data
        # row / observation change in query f(X) = n^-1 * transpose(X)X
        result = centered_covariance_query_sensitivity(n=query_shape[0],
                                                       m=query_shape[1],
                                                       c=query_scale[1])
    else:
        print("get_query_row_sensitivity: \
        required query_type in ('identity','covariance')")
        result = None
    return result


'''
    Examples:
        get_query_gamma(feature_scale,
                        (train_size,features),
                        'identity')
        get_query_gamma(feature_scale,
                        (features,features),
                        query_type='covariance'))
'''


def get_query_gamma(query_scale, query_shape, query_type):
    obs, features = query_shape
    if query_type == 'identity':
        # Defined as sup X ||f(X)||F, where ||f(X)||F is the
        # Frobenious norm of the query f(X)
        result = pow(obs * features * query_scale[1], 0.5)
    elif query_type == 'covariance':
        # Defined as m * c^2 Section 4.4 example 1, p17 in [1]
        result = features*pow(query_scale[1], 2)
    else:
        print("get_query_gamma: \
        required query_type in ('identity','covariance')")
        result = None
    return result
