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

def load_submit_data(prefix, due, full_points, refetch_github_list=False, refetch_github_repo='soft'):
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
        for submit in assignment.submits:
            print(f'''\nStudent Name: {submit.student_name}\nRepo: {submit.repo_name}''')
            os.system(f"cd {get_submit_path(assignment.prefix, submit)}")
            open_new_terminal_tab()
            if submit.grade == None:
                user_input = input(f'Grade ({assignment.full_points}%)? ')
            else:
                user_input = input(f'Regrade ({submit.grade}/{assignment.full_points})? ')
            
            if user_input == '':
                pass
            else:
                submit.grade = int(user_input)
            
            assignment.save()
        
        print('End of list, roll over.')

if __name__ == "__main__":
    assignment = load_submit_data(
        prefix='lab2-parta', 
        due='2018-09-18T23:59:59Z',
        full_points=30,
    )

    # assignment = load_submit_data(
    #     prefix='lab4-birthdaytown', 
    #     due='2018-10-04T23:59:59Z',
    #     full_points=105,
    #     refetch_github_list=False
    # )


    for error in ERROR_MESSAGES:
        print(error)
    
    interactive(assignment)