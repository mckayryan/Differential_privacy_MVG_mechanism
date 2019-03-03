# Generate synthea data sets
import subprocess
import datetime
import pandas

import process_synthea_patient_data

# Synthea command and arguments
seed = '12345'
# Set to condition for calculating framingham risk score
age = '20-79'
population = '50000'
# All states of United States of America with population > 10m (US Census 2015)
# 1  	California 	39,144,818
# 2  	Texas 	27,469,114
# 3  	Florida 	20,271,272
# 4  	New York 	19,795,791
# 5  	Illinois 	12,859,995
# 6  	Pennsylvania 	12,802,503
# 7  	Ohio 	11,613,423
# 8  	Georgia 	10,214,860
# 9  	North Carolina 	10,042,802
states = [
    'California',
    'Texas',
    'Florida',
    'New York',
    'Illinois',
    'Pennsylvania',
    'Ohio',
    'Georgia',
    'North Carolina'
]
data_location = 'synthea/output/csv/'
target_dir = 'data/'

# Install synthea dependencies
print('Installing synthea dependencies...')
subprocess.call(['./gradlew',
                 'build',
                 'check',
                 'test'],
                cwd='synthea')
print('... complete')


for state in states:
    print('Generating data with parameters...')
    print(' '.join(['./run_synthea',
                    '-s', seed,
                    '-a', age,
                    '-p', population,
                    state]))

    subprocess.call(['./run_synthea',
                     '-s', seed,
                     '-a', age,
                     '-p', population,
                     state],
                    cwd='synthea')

    print('... complete')

    target_file_name = '_'.join([state,
                                 population,
                                 datetime.date.today().strftime("%Y%m%d")])

    print('Process data to {%loc}...'.format(
        loc=''.join([target_dir, target_file_name])))

    process_synthea_patient_data(data_dir=data_location,
                                 data_save_dir=target_dir,
                                 data_save_name=target_file_name)

    print('... complete')

    print('Results')
    print(target_file_name,
          len(pandas.read_pickle(''.join([target_dir,
                                          target_file_name]))))

    print('Deleting fhir files...')

    cmd = 'find . -maxdepth 1 -name "*.json" -print0 | xargs -0 rm'
    ps = subprocess.Popen(cmd,
                          shell=True,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT,
                          cwd='synthea/output/fhir')
    ps.communicate()[0]

    subprocess.call(['ls',
                     '/synthea/output/fhir'])

    print('Deleting csv files...')

    cmd = 'find . -maxdepth 1 -name "*.csv" -print0 | xargs -0 rm'
    ps = subprocess.Popen(cmd,
                          shell=True,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT,
                          cwd='synthea/output/csv')
    ps.communicate()[0]

    subprocess.call(['ls',
                     '/synthea/output/csv'])

    print('... complete')
