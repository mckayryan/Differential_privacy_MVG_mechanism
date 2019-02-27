

# Framingham risk score for 10 year cardiovascular disease risk
def calculate_framingham_risk_score(df, column_name):
    '''
        Example query call for framingham_10year_risk

        framingham_10year_risk(sex="M",
                               age=26,
                               total_cholesterol=152,
                               hdl_cholesterol=70,
                               systolic_blood_pressure=130,
                               smoker=True,
                               blood_pressure_med_treatment=False)
    '''
    from framingham10yr.framingham10yr import framingham_10year_risk

    required = [
        'sex',
        'age',
        'total_cholesterol',
        'hdl_cholesterol',
        'systolic_blood_pressure',
        'smoker',
        'blood_pressure_med_treatment'
    ]

    if all(elem in df.columns.values for elem in required):
        df[column_name] = \
            df.apply(lambda d:
                     framingham_10year_risk(
                         sex=d.sex,
                         age=int(d.age),
                         total_cholesterol=int(d.total_cholesterol),
                         hdl_cholesterol=int(d.hdl_cholesterol),
                         systolic_blood_pressure=int(d.systolic_blood_pressure),
                         smoker=d.smoker,
                         blood_pressure_med_treatment=d.blood_pressure_med_treatment
                     ).get('points'),
                     axis=1)
    else:
        print('DataFrame does not contain all required values \
        for function framingham_10year_risk')
        print('Contains {c}'.format(c=df.columns.values))
        print('Requires {r}'.format(r=['sex (str)',
                                       'age (str)',
                                       'total_cholesterol (int/float)',
                                       'hdl_cholesterol (int/float)',
                                       'systolic_blood_pressure (int/float)',
                                       'smoker (bool)',
                                       'blood_pressure_med_treatment (bool)']))
    return df
