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

import os

from utilities import *
from track import *
from github_api import *
from mass_clone import *
from google_spreadsheet_api import *
from github_use_personal_repo import *

from utilities import *
from mass_clone import *

# see more at https://gist.github.com/bobthecow/757788
def get_submit_path(assignment_prefix, submit):
    return ALL_ASSIGNMENT_DIRECTORY_PATH / assignment_prefix / submit.repo_name

def get_graded_number(assignment):
    return len([ s for s in assignment.submits if s.grade ])

def load_submit_data(prefix, due='', full_points='', github_config={}, sheet_api=None, is_cloning_repo=True):
    if sheet_api == None:
        print("ERROR: sheet_api is None, but we need a sheet api instance.")
        exit(1)

    assignment = Assignment(
        prefix=prefix, 
        due=due,
        full_points=full_points,
    )

    # if no submit data at local, definitely download from Github; otherwise if specified
    refetch_github_list = github_config.get('refetch_repo_list', False)
    repo_clone_mode = github_config.get('clone_repo_mode', None)
    use_personal_repo_config = github_config.get('use_personal_repo', {})
    if (len(assignment.submits) == 0 or refetch_github_list):
        print('INFO: Downloading meta data from Github...')
        if not use_personal_repo_config:
            raw_api_data = get_api_data(prefix)
            assignment_api_submit_data = filter_submit_from_api_data(raw_api_data, prefix, sheet_api)
            assignment.deserialize_submits(assignment_api_submit_data)
        else:
            sheet_api = use_personal_repo_config['sheet_api']
            sheet_range = use_personal_repo_config['sheet_range']
            use_personal_repo_submit_data = GithubUsePersonalRepo(sheet_api).get_personal_submits_data(prefix, sheet_range)
            assignment.deserialize_submits(use_personal_repo_submit_data)

    repo_additional_command = github_config.get('repo_additional_command', ';')
    print('\nINFO: Cloning submits...')
    if not is_cloning_repo:
        print(f"INFO: since not batch processing, we won't clone any repo now; is_cloning_repo is {is_cloning_repo}")
    elif repo_clone_mode == 'hard':
        # wipe and reclone
        wipe_repo(prefix)
        mass_clone(prefix, assignment.submits, repo_additional_command)
    elif repo_clone_mode == 'soft':
        mass_clone(prefix, assignment.submits, repo_additional_command)

    assignment.save()
    return assignment

def interactive_assignment_setup(_config={}):
    user_input = input('WARNING: This script will batch clone repo if not done yet, you might want to use in a public computer due to the heavy read/write on your computer disk. Proceed? (Y/n) ')
    if user_input.lower() == 'n':
        exit(0)

    # get assignment prefix
    previous_session_prefix_input = restore_session_dict('session.json')
    if previous_session_prefix_input and previous_session_prefix_input['prefix']:
        previous_session_prefix_input = previous_session_prefix_input['prefix']
        user_input = input(f'\nWARNING: Will start fetching repos. Before that, please enter assignment prefix ({previous_session_prefix_input}): ')
    else:
        user_input = input(f'\nWARNING: Will start fetching repos. Before that, please enter assignment prefix: ')
    if previous_session_prefix_input and user_input == '':
        user_input = previous_session_prefix_input
    elif not previous_session_prefix_input and user_input == '':
        print('No assignment prefix provided. Script terminated.')
        exit(0)
    else:
        store_session_dict({'prefix': user_input}, 'session.json')
    
    # try to use local config for that assignment
    local_configs = restore_session_dict("local-config.json")
    if user_input in local_configs:
        config = { **_config, **local_configs[user_input] }
    else:
        config = _config

    # Ready to create assignment object
    print('\nINFO: Loading submits...')
    spreadsheet_id = config.get('spreadsheet_id', None)
    sheet_tab_name = config.get('sheet_tab_name', None)
    sheet_tab_ranges = config.get('sheet_tab_ranges', {})
    is_batch_processing = config.get('is_batch_processing', True)
    grade_additional_command = config.get('grade_additional_command', ';')
    sheet_api = SheetAPI(spreadsheet_id, sheet_tab_name, sheet_tab_ranges)
    github_config = config.get('github_config', {})
    
    if github_config.get('use_personal_repo', ''):
        github_config['use_personal_repo']['sheet_api'] = sheet_api

    mode = config.get('skip-mode', 'default')
    assignment = load_submit_data(
        prefix=user_input, 
        github_config=github_config,
        sheet_api=sheet_api,
        is_cloning_repo=is_batch_processing
    )
    
    clear_and_prompt_error()

    if not assignment.full_points:
        user_input = input('\nNo assignment full points in cache, please provide: ')
        assignment.full_points = int(user_input)
        assignment.save()
    
    if not assignment.due:
        user_input = input('\nNo assignment due in cache, please provide in format YYYY-MM-DD (Will always use 23:59:59 as time): ')
        assignment.due = Serializer.deserialize_time(f'{user_input}T23:59:59Z')
        assignment.save()
    
    print(f'\nFor each repo, we will open the repo folder in vscode for you, and let you input grade and comment. But, you can always edit grade or comment manually later in data/records.')
    print('\n---Assignment Info---')
    print(f'Assignment: {assignment.prefix}\nDue: {assignment.due}\nFull Points: {assignment.full_points}\nSubmits Total: {len(assignment.submits)}\nGraded: {get_graded_number(assignment)}\nMode: {mode}\nBatch Grading: {is_batch_processing}\n---------------------')
    user_input = input('\nConfirm if the assignment info is correct? (Y/n) ')

    if user_input == '' or user_input.lower() == 'y':
        if is_batch_processing:
            batch_grade_submit(assignment, sheet_api, mode=mode, grade_additional_command=grade_additional_command)
        else:
            single_grade_submit(assignment, sheet_api, mode=mode, 
                grade_additional_command=grade_additional_command, 
                repo_additional_command=github_config.get('repo_additional_command', ';'),
                clone_repo_mode=github_config.get('clone_repo_mode', 'soft')
            )
    else:
        record_file_path = DATA_FOLDER_PATH / 'records' / f'record-{assignment.prefix}.json'
        print('\nPlease correct the assignment info manually in {}'.format(
            record_file_path
        ))
        print('INFO: Script terminated.')

def single_grade_submit(assignment, sheet_api, mode='default', grade_additional_command=';', repo_additional_command=';', clone_repo_mode='soft'):
    roster = sheet_api.get_roster_by_key('uniqname')
    round_count = 0
    submits_total = len(assignment.submits)
    while True:
        user_input = input('Enter student\'s uniqname: ')
        print(f'INFO: student full name: {roster[user_input]["full_name"]}')
        print(f'INFO: student github account: {roster[user_input]["github_account"]}')
        if user_input:
            target_submit = None
            for submit in assignment.submits:
                if submit.github_account == roster[user_input]['github_account']:
                    target_submit = submit
                    break
            
            if target_submit:
                if clone_repo_mode == 'soft':
                    single_clone(assignment.prefix, target_submit, repo_additional_command)
                elif clone_repo_mode == 'hard':
                    wipe_repo(assignment.prefix, student_repo_name=target_submit.repo_name)
                    single_clone(assignment.prefix, target_submit, repo_additional_command)

                round_count = grade_submit(assignment, target_submit, sheet_api, submits_total, round_count, mode, grade_additional_command)
            else:
                print(f"INFO: no submit record for {user_input}")


def batch_grade_submit(assignment, sheet_api, mode='default', grade_additional_command=';'):
    i = 0
    submits_total = len(assignment.submits)
    while i < submits_total:
        submit = assignment.submits[i]
        # mode
        if mode == 'skip-issue':
            if submit.comment:
                i += 1
                continue
        elif mode == 'skip-issue-graded':
            if submit.comment or submit.grade:
                i += 1
                continue

        i = grade_submit(assignment, submit, sheet_api, submits_total, i, mode, grade_additional_command)
    
    print('\nINFO: Finishing looping through all submits.')
    print('\nINFO: Script finished without error.')

def grade_submit(assignment, submit, sheet_api, submits_total, i, mode='default', grade_additional_command=';'):
    # Info
    print(f'''\n-----Grading {i+1}th/{submits_total}, Graded {get_graded_number(assignment)}-----\nStudent Name: {submit.student_name}\nRepo: {submit.repo_name}\nComment: {submit.comment}\nGrade: {submit.grade}/{assignment.full_points}\n''')
    os.system(f"cd {get_submit_path(assignment.prefix, submit)}")

    # Skip?
    edit_everything = False
    if submit.grade != None:
        user_input = input('Already graded, press s to skip or considder other action (S=skip, p=previous, e=edit): ')
        if user_input.lower() == 's' or user_input == '':
            i += 1
            return i
        elif user_input.lower() == 'p':
            if i == 0:
                pass
            else:
                i -= 1
            return i
        elif user_input.lower() == 'e':
            edit_everything = True

    # Run Code
    # command_exec_in_submit(assignment.prefix, submit, 'node -v')

    # Inspect code
    if not grade_additional_command:
        command_exec_in_submit(assignment.prefix, submit, 'code .')
    else:
        command_exec_in_submit_in_terminal(assignment.prefix, submit, grade_additional_command)

    # Grading
    if submit.grade == None:
        user_input = input(f'Grade (full_points={assignment.full_points}, press enter to skip, d=delete grade, p=back to previous student submit. To comment at the same time, type\':\' after grade and type in comment): ')
    else:
        user_input = input(f'Regrade (currently={submit.grade}/{assignment.full_points}), press enter to skip, d=delete grade. To comment, type\':\' after grade and type in comment):  ')
    
    if user_input == '':
        pass
    elif user_input == 'd':
        submit.grade = None
    elif user_input.lower() == 'p':
        if i == 0:
            pass
        else:
            i -= 1
        return i
    elif ':' in user_input:
        tokens = user_input.split(':')
        submit.grade = int(tokens[0])
        submit.comment = ''.join(tokens[1:])
    else:
        submit.grade = int(user_input)
    
    # Commenting
    if not submit.grade or edit_everything:
        user_input = input(f'Enter comment (enter to skip, d=delete comment): ')
        if user_input != '' and user_input.lower() != 'd':
            submit.comment = user_input
        elif user_input.lower() == 'd':
            submit.comment = None
    
    print('\n======')
    
    assignment.save()

    sheet_api.upload_all_records()
    i += 1
    return i
