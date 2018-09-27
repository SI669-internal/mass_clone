from pathlib import Path
import os

ALL_ASSIGNMENT_PATH = Path(__file__).resolve().parent.parent.parent

def mass_clone(assignment_prefix, submit_list):
    # initializing assignment
    assignment_prefix_directory_path = get_assignment_path(assignment_prefix)
    try:
        assignment_prefix_directory_path.mkdir()
    except:
        pass
    
    # initalizing each submit
    for submit in submit_list:
        clone_url = submit.clone_url
        repo_path = assignment_prefix_directory_path / submit.repo_name

        if repo_path.exists():
            pass
        else:
            command = f'git clone {clone_url}'   
            os.system(f"cd {assignment_prefix_directory_path.resolve()} && {command}")

def get_assignment_path(assignment_prefix):
    return ALL_ASSIGNMENT_PATH / assignment_prefix


def wipe_all_repo(assignment_prefix):
    assignment_prefix_directory_path = get_assignment_path(assignment_prefix)
    os.system(f"cd {ALL_ASSIGNMENT_PATH.resolve()} && rm -rf {assignment_prefix}")
    

if __name__ == "__main__":
    pass