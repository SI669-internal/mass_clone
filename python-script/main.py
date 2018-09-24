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

from credentials import *


def get_api_data():
    data_folder = pathlib.Path.cwd() / '..' / 'data'
    response_data_path = data_folder / 'response.json'
    response_data = ''
    
    if response_data_path.exists():
        print("INFO: Reading from cache...")
        response_data = response_data_path.read_text()
        response_data = json.loads(response_data)
    else:
        # Github API https://developer.github.com/v3/repos/#list-your-repositories
        response = get('https://api.github.com/orgs/SI669-classroom/repos', auth=(os.environ['GITHUB_USER'], os.environ['GITHUB_PASSWORD']))
        response_data = response.json()

        # cache
        response_data_path.write_text(json.dumps(response_data))
    
    return response_data

def get_submit_data(api_data):
    assignment = 'lab2-parta'
    due_at = datetime.datetime(year=2018, month=9, day=18, hour=11, minute=59, second=59, microsecond=999)

    submit_data = []

    for data in api_data:
        clone_url = data['clone_url']
        submitted_at = datetime.datetime.strptime(data['updated_at'], '%Y-%m-%dT%H:%M:%SZ')
        repo_name = data['name']
        is_late = submitted_at > due_at 
        late_delta = submitted_at - due_at if is_late else ''

        submit_data.append({
            'clone_url': clone_url,
            'submitted_at': submitted_at,
            'repo_name': repo_name,
            'is_late': is_late,
            'late_delta': late_delta
        })
    
    return submit_data


if __name__ == "__main__":
    

    api_data = get_api_data()
    submit_data = get_submit_data(api_data)

    for data in submit_data:
        print(data['clone_url'], data['submitted_at'], data['repo_name'], data['is_late'], data['late_delta'], '\n')
    print('Total {} records'.format(len(submit_data)))
