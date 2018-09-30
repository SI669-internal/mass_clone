from interactive import *

if __name__ == '__main__':
    interactive_assignment_setup({
        # (optional) options: 'skip-issue-graded', 'skip-issue', 'default'
        'mode': 'skip-issue-graded', 

        'github_config': {
            # (optional) 
            # 'refetch_repo_list': True,

            # (optional) 
            # 'clone_repo_mode': 'soft', 
            
            # Please setup `use_personal_repo` if repo is not using Github Classroom 
            # If using Github Classroom, please comment out `use_personal_repo`
            'use_personal_repo': {
                'sheet_range': 'lab2_partb_personal_repo!D1:R' # specify the range where the personal repo info are. See example at https://docs.google.com/spreadsheets/d/1jZOmd0lkXcllnhtk3DmC7oSM5Q_4H7R-pO9Wy-ydzKo/edit#gid=1501573164
            },

            # (optional) after repo cloned, this code will run in shell environment. Already cd to repo directory for you.
            'repo_additional_command': 'if [ -f ./package.json ]; then npm i; fi'
        },

        # (optional) when grading in interactive console, for each grading, run this code first. Already cd to repo directory for you.
        'grade_additional_command': 'ng serve --open'
    })