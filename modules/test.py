
import os


path = os.environ.get('PROJECT_PATH', '.')

list_of_files = os.listdir(f'{path}/data/models/')

def file_date(x):
    return x[-12:]

latest_file = sorted(list_of_files, key=file_date)[-1]
print(latest_file)