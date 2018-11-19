from pathlib import Path
import json

DATA_FOLDER_PATH = Path(__file__).resolve().parent.parent / 'data'
ALL_ASSIGNMENT_DIRECTORY_PATH = Path(__file__).resolve().parent.parent.parent

ERROR_MESSAGES = []

def clear_and_prompt_error():
    global ERROR_MESSAGES
    
    if (len(ERROR_MESSAGES)) == 0:
        return
    
    for err in ERROR_MESSAGES:
        print(ERROR_MESSAGES)
    ERROR_MESSAGES = []
    user_input = input('\nWARNING: Please check the error message(s) above. Proceed? (Y/n) ')
    if user_input.lower() != 'y' and user_input != '':
        exit(0)

def store_session_dict(dictionary_data, file_name):
    file_path = Path(__file__).parent / 'script-session' / file_name
    with file_path.open(mode='w') as f:
        json.dump(dictionary_data, f, sort_keys=True, indent=4)

def restore_session_dict(file_name):
    file_path = Path(__file__).parent / 'script-session' / file_name
    try:
        with file_path.open(mode='r') as f:
            return json.load(f)
    except:
        return {}

try:
    from credentials import *
except:
    pass
