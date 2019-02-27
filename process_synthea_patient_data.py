# Package imports
import pandas
import numpy

# Local imports
from calculate_framingham_risk_score import calculate_framingham_risk_score


def sample_from_key_to_unique(data, key):
    '''
    Requires:
       data        - Pandas DataFrame
       key         - Column of "data" to be sampled from

    Returns:
       result      - Pandas DataFrame single entry per unique value of "key"
                     from "data" sampled randomly
    '''
    # Distinct list of keys
    unique = data[key].unique()

    result = data.truncate(before=-1, after=-1).copy()
    # Sample one entry from each key
    for value in unique:
        result = pandas.concat([
            result,
            data.loc[data[key] == value].sample(1)
        ])

    return result


def process_synthea_patient_data(data_dir,
                                 data_save_dir,
                                 data_save_name):

    data = dict()
    paths = dict()
    datasets = [
        'patients',
        'observations',
        'medications'
    ]

    # Import csv data
    for d in datasets:
        paths[d] = data_dir + d + '.csv'
        data[d] = pandas.read_csv(paths[d]).rename(str.lower, axis='columns')

    features = [
        'Systolic Blood Pressure',
        'Diastolic Blood Pressure',
        'Tobacco smoking status NHIS',
        'Body Mass Index',
        'Glucose',
        'Triglycerides',
        'High Density Lipoprotein Cholesterol',
        'Total Cholesterol',
        'Low Density Lipoprotein Cholesterol'
    ]

    '''
        Process MEDICATIONS data
    '''
    # Gather examples of medication for 'Hypertension' or high blood pressure
    data['medications'].dropna(inplace=True)

    data['hypertension'] = (data['medications']
                            .loc[data['medications']['reasondescription']
                                 .str.contains('Hypertension'),
                                 ['start', 'stop', 'patient']])

    del data['medications']

    data['hypertension'] = (data['hypertension']
                            .assign(blood_pressure_med_treatment=True))

    '''
        Process PATIENTS data
    '''
    data['patients'] = (data['patients'][['id', 'birthdate', 'gender']]
                        .rename({'id': 'patient', 'gender': 'sex'},
                                axis='columns'))

    data['patients'].dropna(inplace=True)

    '''
        Process OBSERVATIONS data
    '''
    data['observations']['description'].dropna(inplace=True)

    new_feature = (data['observations']['description']
                   .str.split(r'(\-|\[.*\])', n=1, expand=True))

    data['observations'] = (data['observations']
                            .assign(feature=new_feature[0]
                                    .str.strip()))

    data['obs features'] = (data['observations']
                            .loc[data['observations']['feature']
                                 .isin(features),
                                 ['date', 'patient', 'encounter',
                                  'feature', 'value']])

    del data['observations']

    data['obs features'].dropna(inplace=True)

    # Process numerical features
    data['obs floats'] = data['obs features'][data['obs features']['value']
                                              .str.contains(r'^[\d\.]+$')]

    data['obs floats'] = (data['obs floats']
                          .assign(value=data['obs floats']['value']
                                  .astype(float)))

    # Process categorical features
    # Gather examples of smokers
    data['smokers'] = (data['obs features']
                       .loc[data['obs features']['feature']
                            .str.contains('Tobacco smoking status NHIS'),
                            ['encounter', 'patient', 'value']])

    data['smokers'] = (data['smokers']
                       .replace({'Former smoker': True,
                                 'Never smoker': False,
                                 'Current every day smoker': True})
                       .rename({'value': 'smoker'}, axis='columns'))

    # Transpose such that features are columns with 'value as their values
    data['features'] = (data['obs floats']
                        .pivot_table(index=['date', 'encounter', 'patient'],
                                     columns='feature', values='value')
                        .reset_index()
                        .dropna()
                        .copy())

    del data['obs floats']

    # Merge 'patient', 'obserservations',  'smoker' and 'hypertension' data

    # Combine patient and observation data
    data['features'] = pandas.merge(data['features'], data['patients'],
                                    how='left', on='patient')

    # Combine with smoker status
    merged = pandas.merge(data['features'], data['smokers'],
                          how='left', on=['encounter', 'patient']).copy()

    # Combine with hypertention medication status
    merged = pandas.merge(merged, data['hypertension'],
                          how='left', on='patient')

    data['features'] = merged[
        (merged['start'].isnull() |
            ((merged['start'] <= merged['date']) &
             (merged['stop'] >= merged['date']))
         )]

    del merged, data['patients'], data['hypertension'], data['smokers']

    data['features'] = (
        data['features']
        .assign(blood_pressure_med_treatment=data['features'][
            'blood_pressure_med_treatment']
            .fillna(False)))

    # Clean feature names
    new_feature_names = {
        'Body Mass Index': 'bmi',
        'Total Cholesterol': 'total_cholesterol',
        'High Density Lipoprotein Cholesterol': 'hdl_cholesterol',
        'Low Density Lipoprotein Cholesterol': 'ldl_cholesterol',
        'Systolic Blood Pressure': 'systolic_blood_pressure',
        'Diastolic Blood Pressure': 'diastolic_blood_pressure'
    }

    data['features'] = (data['features']
                        .rename(new_feature_names, axis='columns')
                        .rename(str.lower, axis='columns'))

    # Derived features
    # Age at time of observation
    data['features'] = data['features'].assign(age=(
        numpy.subtract(
            pandas.to_datetime(data['features'].date),
            pandas.to_datetime(data['features'].birthdate)))
        .dt.days / 365.25)

    # Framingham scoreA
    data['features'] = calculate_framingham_risk_score(data['features'],
                                                       'framingham')

    # Randomly sample from key 'patients' to create unique entry for each
    data['unique_features'] = sample_from_key_to_unique(
        data=data['features'],
        key='patient')

    # Pickle data to supplied location
    data['unique_features'].to_pickle(data_save_dir + data_save_name)

    return data['unique_features']
