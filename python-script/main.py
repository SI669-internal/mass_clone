from requests import get # http://docs.python-requests.org/en/master/
import json
import datetime
import pathlib # https://realpython.com/python-pathlib/
'''
# Generate path object (several ways)
path = pathlib.Path.cwd() / 'some_directory' / 'test.md'
path = pathlib.Path('test.md')
'''
'''
# Write / Read file (several ways)
with path.open(mode='r') as reading_file:
    pass

path.read_text()
path.write_text()
'''
'''
# Comparing paths
path.resolve().parent == pathlib.Path.cwd()
'''
'''
path.name # 'test.md'
path.stem # 'test'
path.suffix # '.md'
path.parent.parent... # return Path object
path_objecy / 'directory' / 'filename' # return Path object
'''
'''
path.exists() # True / False
path.replace(another_path) # Will move file to that path. Will overwirte file if exists!
'''

import csv # https://realpython.com/python-csv/

from script_settings import *
from roster import *

def get_datetime_now_iso_string():
    return datetime.datetime.now().strftime('%Y-%m-%dT%H-%M-%SZ')

def get_api_data():
    response_files_check = DATA_FOLDER_PATH.glob('response*.json')
    for response_file_path in response_files_check:
        backup_data_folder_path = DATA_FOLDER_PATH / 'backup'
        response_file_path.replace(backup_data_folder_path / response_file_path.name)

    # Github API https://developer.github.com/v3/repos/#list-your-repositories
    response = get('https://api.github.com/orgs/SI669-classroom/repos', auth=(os.environ['GITHUB_USER'], os.environ['GITHUB_PASSWORD']))
    response_data = response.json()

    # cache
    response_data_path = DATA_FOLDER_PATH / 'response-{}.json'.format(get_datetime_now_iso_string())
    response_data_path.write_text(json.dumps(response_data))
    
    return response_data

def get_submit_data(raw_api_data, assignment_identifier):
    api_data = raw_api_data
    due_at = datetime.datetime(year=2018, month=9, day=18, hour=11, minute=59, second=59, microsecond=999)
    student_roster = get_student_roster()
    submit_data = []

    assignment_api_data = []
    for data in api_data:
        if data['name'].startswith(assignment_identifier):
            repo_name = data['name']
            github_account = repo_name.split('-')[-1]
            if (
                github_account != 'kchetan92' and
                github_account != 'rivernews'
                ):
                data['github_account'] = github_account
                data['repo_name'] = repo_name
                assignment_api_data.append(data)

    for data in assignment_api_data:
        clone_url = data['clone_url']
        submitted_at = datetime.datetime.strptime(data['updated_at'], '%Y-%m-%dT%H:%M:%SZ')
        student_name = student_roster[data['github_account']]['student_name']
        is_late = submitted_at > due_at 
        late_delta = submitted_at - due_at if is_late else None

        submit_data.append({
            'clone_url': clone_url,
            'submitted_at': submitted_at,
            'repo_name': data['repo_name'],
            'is_late': is_late,
            'late_delta': late_delta,
            'github_account': data['github_account'],
            'student_name': student_name
        })
    
    return submit_data


if __name__ == "__main__":

    api_data = get_api_data()
    submit_data = get_submit_data(api_data, 'lab2-parta')

    for data in submit_data:
        print(data, '\n')
    print('Total {} records'.format(len(submit_data)))
