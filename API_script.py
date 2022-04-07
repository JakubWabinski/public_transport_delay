import pandas as pd
import requests
import time
import json
import os
import logging

from datetime import datetime

apikey = 'ed51695c-0f7b-45ed-a3d5-2eae45e84a68'
resource_id = 'f2e5503e-927d-4ad3-9500-4ab9e55deb59'

vehicle_type = input('Wpisz "1" dla autobusów lub "2" dla tramwajów ')
target_time = input('Do kiedy zbierać dane? (YYYY-MM-DD HH:MM:SS)')

link = 'https://api.um.warszawa.pl/api/action/busestrams_get/?resource_id=%20' + 'f2e5503e-927d-4ad3-9500-4ab9e55deb59'\
    + '&apikey=' + apikey \
    + '&type=' + vehicle_type

requested_data = requests.get(link)
json_dictionary = requested_data.json()
df = pd.json_normalize(json_dictionary['result'])

current_time = datetime.strptime(df['Time'][0], '%Y-%m-%d %H:%M:%S')
match_time = datetime.strptime(target_time, '%Y-%m-%d %H:%M:%S')
os.chdir((os.path.join(os.getcwd() + '\\output')))
os.makedirs(os.path.join(os.getcwd(), str(current_time.month) + '_' + str(current_time.year)), exist_ok=True)
os.chdir((os.path.join(os.getcwd(), str(current_time.month) + '_' + str(current_time.year))))
cwd = os.getcwd()

print(current_time)
print(match_time)
print(cwd)

match_time = datetime.strptime(target_time, '%Y-%m-%d %H:%M:%S')

while current_time < match_time:
    try:
        requested_data = requests.get(link)
        json_dictionary = requested_data.json()
        df = pd.json_normalize(json_dictionary['result'])
        current_time = datetime.strptime(df['Time'][0], '%Y-%m-%d %H:%M:%S')
        file_name = 'trams_' + str(current_time.year) + '_' + str(current_time.month) + '_' + str(current_time.day) + '_' + str(current_time.hour) + '.txt'
        with open(os.path.join(cwd, file_name), 'a') as f:
            f.write('\n' + str(current_time) + '\n')
            json.dump(json_dictionary, f)
            f.write('\n\n')
            f.close()
            time.sleep(30)
            new_time = datetime.strptime(df['Time'][0], '%Y-%m-%d %H:%M:%S')
            if new_time.day != current_time.day:
                os.chdir('..')
                os.makedirs(os.path.join(os.getcwd(), str(new_time.month) + '_' + str(new_time.year)), exist_ok=True)
                cwd = os.chdir((os.path.join(os.getcwd(), str(new_time.month) + '_' + str(new_time.year))))
                print('New day begins...')
    except AttributeError as err:
        print('Attribute Error occurred at... ' + str(current_time) + '\n' + str(logging.exception(err)))
        continue
    except (ConnectionError, TimeoutError) as err:
        print('Connection Error occurred at... ' + str(current_time) + '\n' + str(logging.exception(err)))
        continue
    except OSError as err:
        print('OS Error occurred at... ' + str(current_time) + '\n' + str(logging.exception(err)))
        continue
