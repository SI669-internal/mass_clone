from requests import get # http://docs.python-requests.org/en/master/
import json
import datetime
import pathlib # https://realpython.com/python-pathlib/

from utilities import *
from roster import *

def get_datetime_now_iso_string():
    return datetime.datetime.now().strftime('%Y-%m-%dT%H-%M-%SZ')

def github_search_api(assigment_prefix):
    json_data = get('https://api.github.com/search/repositories',  # search q https://help.github.com/articles/searching-for-repositories/#search-within-a-users-or-organizations-repositories
        auth=(os.environ['GITHUB_USER'], os.environ['GITHUB_PASSWORD']),
        params={
            'per_page': '99',
            'q': f'{assigment_prefix}+org:SI669-classroom'
        }
    ).json()

    # items = json_data.get('items')

    # discovered_total = json_data.get('total_count')
    # got_total = len(items)

    return json_data.get('items')

def filter_submit_from_api_data(api_data, assignment_prefix, sheet_api):
    assignment_api_data = []
    student_roster = get_student_roster_by_sheet(sheet_api)
    
    for data in api_data:
        # filter only this assingment
        if data['name'].startswith(assignment_prefix):
            repo_name = data['name']
            github_account = repo_name.split('-')[-1]

            # exclude instructors
            if (
                github_account != 'kchetan92' and
                github_account != 'rivernews' and
                github_account != 'numerator'
                ):
                
                # append useful entry
                data['github_account'] = github_account
                data['repo_name'] = repo_name
                try:
                    data['student_name'] = student_roster[github_account]['student_name']
                    assignment_api_data.append(data)
                except:
                    ERROR_MESSAGES.append(f"ERROR: Github account cannot resolve who: {github_account} for submitted repo: {repo_name}, after comparing w/ the roster in sheet.")
    
    return assignment_api_data

def get_api_data(assigment_prefix):
    response_files_check = DATA_FOLDER_PATH.glob('response*.json')
    for response_file_path in response_files_check:
        backup_data_folder_path = DATA_FOLDER_PATH / 'backup'
        response_file_path.replace(backup_data_folder_path / response_file_path.name)

    # Github API https://developer.github.com/v3/repos/#list-your-repositories
    print('INFO: Downloading meta data from Github...')

    # response = get('https://api.github.com/orgs/SI669-classroom/repos', 
    #     auth=(os.environ['GITHUB_USER'], os.environ['GITHUB_PASSWORD']),
    #     params={
    #         'type': 'all',
    #         'per_page': 90
    #     }
    # )
    # response_data = response.json()

    response_data = github_search_api(assigment_prefix)

    print(f'INFO: Total {len(response_data)} entries.')

    # cache
    response_data_path = DATA_FOLDER_PATH / 'response-{}.json'.format(get_datetime_now_iso_string())
    response_data_path.write_text(json.dumps(response_data))
    
    return response_data