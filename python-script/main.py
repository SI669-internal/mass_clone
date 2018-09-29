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

from script_settings import *
from roster import *
from track import *
from github_api import *
from mass_clone import *
from google_spreadsheet_api import *

ERROR_MESSAGES = []

# see more at https://gist.github.com/bobthecow/757788
def open_new_terminal_tab():
    os.system("osascript -e 'tell application \"iTerm\" to activate' -e 'tell application \"System Events\" to tell process \"iTerm\" to keystroke \"t\" using command down'")

def filter_submit_from_api_data(api_data, assignment_prefix):
    assignment_api_data = []
    student_roster = get_student_roster()
    
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
                    ERROR_MESSAGES.append(f"ERROR: Github account cannot resolve who: {github_account} for submitted repo: {repo_name}")
                
    
    return assignment_api_data

def load_submit_data(prefix, due='', full_points='', refetch_github_list=False, refetch_github_repo='soft'):
    assignment = Assignment(
        prefix=prefix, 
        due=due,
        full_points=full_points,
    )

    # if no submit data at local, definitely download from Github
    if (len(assignment.submits) == 0 or refetch_github_list):
        raw_api_data = get_api_data(prefix)
        assignment_api_submit_data = filter_submit_from_api_data(raw_api_data, prefix)
        assignment.deserialize_submits(assignment_api_submit_data)

        if refetch_github_repo == 'hard':
            # wipe and reclone
            wipe_all_repo(prefix)
            mass_clone(prefix, assignment.submits)
        elif refetch_github_repo == 'soft':
            mass_clone(prefix, assignment.submits)

    
    assignment.save()
    return assignment

def get_submit_path(assignment_prefix, submit):
    return ALL_ASSIGNMENT_PATH / assignment_prefix / submit.repo_name

def interactive(assignment):
    while True:
        submits_total = len(assignment.submits)
        i = 0
        while True:
            submit = assignment.submits[i]
            # Info
            graded_number = len([ s for s in assignment.submits if s.grade ])
            print(f'''\n-----Grading {i+1}th/{submits_total}, Graded {graded_number}-----\nStudent Name: {submit.student_name}\nRepo: {submit.repo_name}\nComment: {submit.comment}\nGrade: {submit.grade}/{assignment.full_points}\n''')
            os.system(f"cd {get_submit_path(assignment.prefix, submit)}")

            # Skip?
            edit_everything = False
            if submit.grade != None:
                user_input = input('Already graded, press s to skip or considder other action (S=skip, p=previous, e=edit): ')
                if user_input.lower() == 's' or user_input == '':
                    i += 1
                    continue
                elif user_input.lower() == 'p':
                    if i == 0:
                        pass
                    else:
                        i -= 1
                    continue
                elif user_input.lower() == 'e':
                    edit_everything = True

            # Run Code
            # command_exec_in_submit(assignment.prefix, submit, 'node -v')

            # Inspect code
            open_submit_by_vscode(assignment.prefix, submit)

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
                continue
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

            sheet_api = SheetAPI()
            sheet_api.upload_all_records()
            i += 1
        
        print('End of list, roll over.')

if __name__ == "__main__":
    user_input = input('WARNING: This script will batch clone repo if not done yet, you might want to use in a public computer due to the heavy read/write on your computer disk. Proceed? (Y/n) ')
    if user_input.lower() == 'n':
        exit(0)

    # lab2-parta, lab4-birthdaytown
    previous_session_prefix_input = restore_session_dict('prefix.json')
    if previous_session_prefix_input and previous_session_prefix_input['prefix']:
        previous_session_prefix_input = previous_session_prefix_input['prefix']
        user_input = input(f'\nWill start fetching repos. Before that, please enter assignment prefix ({previous_session_prefix_input}): ')
    else:
        user_input = input(f'\nWill start fetching repos. Before that, please enter assignment prefix: ')
    if previous_session_prefix_input and user_input == '':
        user_input = previous_session_prefix_input
    elif not previous_session_prefix_input and user_input == '':
        print('No assignment prefix provided. Script terminated.')
        exit(0)
    else:
        store_session_dict({'prefix': user_input}, 'prefix.json')

    assignment = load_submit_data(
        prefix=user_input, 
        refetch_github_list=False
    )

    for error in ERROR_MESSAGES:
        print(error)

    if not assignment.full_points:
        user_input = input('\nNo assignment full points in cache, please provide: ')
        assignment.prefix = int(user_input)
        assignment.save()
    
    if not assignment.due:
        user_input = input('\nNo assignment due in cache, please provide in format YYYY-MM-DD (Will always use 23:59:59 as time): ')
        assignment.due = Serializer.deserialize_time(f'{user_input}T23:59:59Z')
        assignment.save()
    
    print('\n---Assignment Info---')
    print(f'Assignment: {assignment.prefix}\nDue: {assignment.due}\nFull Points: {assignment.full_points}\n---------------------')
    user_input = input('Confirm if the assignment info is correct? (Y/n) ')

    record_file_path = DATA_FOLDER_PATH / 'records' / f'record-{assignment.prefix}.json'
    if user_input == '' or user_input.lower() == 'y':
        user_input = input(f'\nOK, let\'s start!\nFor each repo, we will open the repo folder in vscode for you, and let you input grade and comment. But, you can always edit grade or comment manually in {record_file_path}. Sounds good? (Y/n) ')
        if user_input.lower() != 'n':
            interactive(assignment)
    else:
        print('\nPlease correct the assignment info manually in {}'.format(
            record_file_path
        ))
        print('INFO: Script terminated.')
    
    