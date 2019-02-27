# TESTS
def test_function(func, test_data, test_expected, **kwargs):
    print('\nTesting function \n"{f}"...'.format(f=func.__name__))
    test_result = func(data=test_data, **kwargs)
    if test_expected.equals(test_result):
        print('... Test passed!!!!\n')
    else:
        print('... Test failed :(')
        print('Expected')
        print(test_expected)
        print('Received...')
        print(test_result)


# Test scale_data
test_params = dict(data_bounds={'Diastolic Blood Pressure': (60, 140),
                                'Glucose': (0, 2000)},
                   target_bounds=(-1, 1))

test_scale_data = pandas.DataFrame({
    'Diastolic Blood Pressure': [60, 100, 120, 140],
    'Glucose': [0, 50, 1000, 2000],
})
test_expected = pandas.DataFrame({
    'Diastolic Blood Pressure': [-1, 0, 0.5, 1],
    'Glucose': [-1, -0.95, 0, 1],
})

test_function(func=scale_data,
              test_data=test_scale_data,
              test_expected=test_expected,
              **test_params)
