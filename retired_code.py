# Model Parameters
sensitivity = get_query_row_sensitivity(query_form='covariance',
                                        query_scale=feature_scale,
                                        data_shape=data.shape)

# Model definition
query = centered_sample_covariance_matrix(X=data)

for _ in xrange(test_samples):
    # Sample mechanism
    start_sample_clock = datetime.datetime.now()
    # Add symmetric iid noise
    sample = gaussian_mechanism_matrix_sample(
        data=query,
        epsilon=epsilon,
        delta=delta,
        sensitivity=sensitivity,
        symmetric=True,
        verbose=False)
    end_sample_clock = datetime.datetime.now()

    if result is None:
        result = pandas.DataFrame([[
            mechanism,
            query_type,
            1,
            metric,
            principle_component_RSS(true=query, pred=sample),
            (end_sample_clock - start_sample_clock).total_seconds()]],
            columns=columns)

    else:
        result = pandas.concat([
            result,
            pandas.DataFrame([[
                mechanism,
                query_type,
                len(result)+1,
                metric,
                principle_component_RSS(true=query, pred=sample),
                (end_sample_clock - start_sample_clock).total_seconds()]],
                columns=columns)
        ])

result.to_pickle(result_pickle_location + result_pickle_name)


# Differential Privacy parameters
epsilon = 1.0
delta = pow(obs, -1)

test_split = 0.1
test_size = int(obs*test_split)
train_size = obs - test_size

# Identity query parameters

# from differential_privacy_parameters import *

params = dict(
    query_scale=feature_scale,
    data_shape=(train_size, features)
)

# Global maximum of change for any single point change in query f(X) = X
unit_sensitivity = abs(numpy.subtract(feature_scale[0], feature_scale[1]))
print('Testing ... unit_sensitivity')
print(unit_sensitivity == get_query_point_sensitivity(query_form='unit', **params))

# Global maximum of change for any data row / observation change in query f(X) = X
# Section 8.1.3 p30 of paper [1]
obs_sensitivity = pow(features*pow(unit_sensitivity, 2), 0.5)
print('Testing ... obs_sensitivity')
print(obs_sensitivity == get_query_row_sensitivity(query_form='unit', **params))

# Defined as sup X ||f(X)||F, where ||f(X)||F is the Frobenious norm of the query f(X)
gamma = pow(train_size*features*feature_scale[1], 0.5)
print('Testing ... gamma')
print(round(gamma, 6) == round(get_query_gamma(feature_scale, (train_size, features), 'unit'), 6))

# Covariance query parameters

# Global maximum of change for a single point change in query f(X) = (1/n)*transpose(X)X
symmetric_unit_sensitivity = centered_covariance_query_sensitivity(n=train_size,
                                                                   m=1.0,
                                                                   c=feature_scale[1])
print('Testing ... symmetric_unit_sensitivity')
print(round(symmetric_unit_sensitivity, 6) == round(
    get_query_point_sensitivity(query_form='covariance', **params), 6))
# Global maximum of change for any data row / observation change in query f(X) = n^-1 * transpose(X)X
symmetric_obs_sensitivity = centered_covariance_query_sensitivity(n=train_size,
                                                                  m=features,
                                                                  c=feature_scale[1])
print('Testing ... symmetric_obs_sensitivity')
print(symmetric_obs_sensitivity == get_query_row_sensitivity(query_form='covariance', **params))
# Defined as m * c^2 Section 4.4 example 1, p17 in [1]
symmetric_gamma = features*pow(feature_scale[1], 2)
print('Testing ... symmetric_gamma')
print(symmetric_gamma == get_query_gamma(feature_scale, (features, features), query_form='covariance'))

print('Differential Privacy Parameters')
print(' '.join([
    '\nSensitivity - Identity Query\n',
    'Unit\t\t', str(unit_sensitivity), '\n',
    'Observation\t', str(obs_sensitivity), '\n',
    'Identity Gamma\t', str(gamma), '\n',
    '\nSensitivity - Covariance Query\n',
    'Unit\t\t', str(symmetric_unit_sensitivity), '\n',
    'Observation\t', str(symmetric_obs_sensitivity), '\n',
    'Covar Gamma\t', str(symmetric_gamma), '\n',
]))


# MAX PNR
params = dict(
    epsilon=epsilon,
    delta=delta,
    query_sensitivity=obs_sensitivity,
    query_sup=gamma,
    #     precision_allocation=feature_allocations[allocation],
    #     precision_direction=numpy.identity(features),
    covariance_direction='unimodal features',
    #     covariance_method='binary',
    sample_shape=X.shape
)

mvg_mechanism = MVGMechanism(
    epsilon=epsilon,
    delta=delta,
    query_sensitivity=obs_sensitivity,
    query_sup=gamma,
    covariance_direction='unimodal features',
    sample_shape=X.shape)

Q, K_sv, Qt = numpy.linalg.svd(centered_sample_covariance_matrix(X=X),
                               full_matrices=True)

# Set covariance matricies for MVG mechanism
# mvg_mechanism.set_covariance(method=covariance_method,
#                              precision_allocation=precision_allocation,
#                              precision_direction=precision_direction)
Q_f, K_f_sv, Q_ft = numpy.linalg.svd(numpy.kron(numpy.transpose(K_f), K_f),
                                     full_matrices=True)


a = self.precision_parameters['alpha']
b = self.precision_parameters['beta']
n, m = self.shape

a = mvg_mechanism.precision_parameters['alpha']
b = mvg_mechanism.precision_parameters['beta']
n, m = X.shape

''' d as defined at the top of p28.
'''
d = (pow(-b + pow(pow(b, 2) + 8*a*epsilon, 0.5), 2) /
     (4*pow(a, 2)))
''' c as defined in Theorm 7. p27. equation 25
'''
c = (d + numpy.sum(pow(K_f_sv, -1))) / (m*n)

''' Derivation from Theorm 7. p27. equation 26
'''
D_z = [c]*len(K_f_sv) - pow(K_f_sv, -1)
D = numpy.diag(pow(D_z, -1))

cov_kron = numpy.matmul(numpy.matmul(Q_ft, D), Q_f)


model = keras_seq_reg_model_compilation(
    features=X_test.shape[1],
    tf_loss=tf.losses.mean_squared_error,
    tf_metrics=[metrics.mean_squared_error,
                metrics.kullback_leibler_divergence,
                metrics.mean_absolute_error])

# Train model
model.fit(X_train,
          y_train,
          epochs=10,
          batch_size=16,
          verbose=0,
          validation_data=(X_test, y_test))

print(root_mean_squared_error(
    model.predict(X_test, batch_size=16),
    y_test))


# Create sequential NN model
model_simple_dp = keras_seq_reg_model_compilation(
    features=X_test.shape[1],
    tf_loss=tf.losses.mean_squared_error,
    tf_metrics=[metrics.mean_squared_error,
                metrics.kullback_leibler_divergence,
                metrics.mean_absolute_error])

# Train model
model_simple_dp.fit(X_simple_dp_train,
                    y_simple_dp_train,
                    epochs=10,
                    batch_size=32,
                    validation_data=(X_test, y_test))
