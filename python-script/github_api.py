from requests import get # http://docs.python-requests.org/en/master/
import json
import datetime
import pathlib # https://realpython.com/python-pathlib/

from script_settings import *

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