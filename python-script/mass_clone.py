from utilities import *
from pathlib import Path
import os

def mass_clone(assignment_prefix, submit_list, repo_additional_command):
    # initializing assignment
    assignment_prefix_directory_path = get_assignment_path(assignment_prefix)
    try:
        assignment_prefix_directory_path.mkdir()
    except:
        pass
    
    global ERROR_MESSAGES
    all_succeed = True
    # initalizing each submit
    for submit in submit_list:
        repo_path = assignment_prefix_directory_path / submit.repo_name
        
        if repo_path.exists():
            pass
        else:
            print('INFO: Cloning git repo...')
            command = f'git clone {submit.clone_url} {repo_path.resolve()}'   
            check_return = os.system(f"cd {assignment_prefix_directory_path.resolve()} && {command}")
            if check_return != 0:
                ERROR_MESSAGES.append(f'ERROR: Failed on git clone. Student Name: {submit.student_name}, clone url: {submit.clone_url}')
                all_succeed = False
            else:
                check_return = os.system(f"cd {repo_path.resolve()} && {repo_additional_command}")
                ERROR_MESSAGES.append(f'ERROR: Failed on additional command. Command: {repo_additional_command}, at repo_path: {repo_path}.') if check_return != 0 else None
                all_succeed = False
    
    if all_succeed:
        print('\nINFO: All repo cloned successfully.')
    else:
        clear_and_prompt_error()
    
def get_assignment_path(assignment_prefix):
    return ALL_ASSIGNMENT_DIRECTORY_PATH / assignment_prefix

def command_exec_in_submit(assignment_prefix, submit, command):
    repo_path = get_assignment_path(assignment_prefix) / submit.repo_name
    os.system(f"cd {repo_path.resolve()} && {command}")

def get_iterm_exec_string_after_e(apple_command):
    return f'''tell application \"System Events\" to tell process \"iTerm\" to {apple_command}'''

def command_exec_in_submit_in_terminal(assignment_prefix, submit, command):
    repo_path = get_assignment_path(assignment_prefix) / submit.repo_name
    
    # open new tab in iterm2
    # os.system("osascript -e 'tell application \"iTerm\" to activate' -e 'tell application \"System Events\" to tell process \"iTerm\" to keystroke \"t\" using command down'")
    # new_terminal_tab_command = "osascript -e 'tell application \"iTerm\" to activate' -e 'tell application \"System Events\" to tell process \"iTerm\" to keystroke \"t\" using command down'"

    command_list = [ f'cd {repo_path.resolve()}', command]
    
    # command_exec_in_repo = f'cd {repo_path.resolve()} && {command}'
    
    iterm_exec_command_list = [ get_iterm_exec_string_after_e(f'keystroke \"{c}\"') for c in command_list ]

    exec_command_collection_string = ''
    for exec_command in iterm_exec_command_list:
        exec_command_collection_string += f'-e \'{exec_command}\' '
        exec_command_collection_string += '-e \'{}\' '.format(get_iterm_exec_string_after_e('key code 52'))
    
    open_iterm_exec_command = f"osascript -e 'tell application \"iTerm\" to activate' -e 'tell application \"System Events\" to tell process \"iTerm\" to keystroke \"t\" using command down' {exec_command_collection_string}"
    # os.system(f'''{new_terminal_tab_command} -e 'tell application \"iTerm\" to do script "cd {repo_path.resolve()} && {command}" in selected tab of the front window'''')
    os.system(open_iterm_exec_command)

    
def wipe_all_repo(assignment_prefix):
    assignment_prefix_directory_path = get_assignment_path(assignment_prefix)
    os.system(f"cd {ALL_ASSIGNMENT_DIRECTORY_PATH.resolve()} && rm -rf {assignment_prefix}")
    

if __name__ == "__main__":
    pass