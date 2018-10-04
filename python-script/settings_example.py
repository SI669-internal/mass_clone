'''
    This File Serve As Script Setting Template

    1. Copy this file and rename as settings_local.py
    2. Modify the parameters in get_script_settings() based on your needs

'''

def get_script_settings():
    return {
        # (optional) available options listed below.
        # 'skip-issue-graded': skip commented submits and graded submits.
        # 'skip-issue': skip commented submits
        # 'default': always ask before skip
        'skip-mode': 'skip-issue-graded',

        # [required] the spreadsheet file you want to work with
        # spread id https://docs.google.com/spreadsheets/d/<ID HERE>/edit..
        'spreadsheet_id': os.environ['SPREADSHEET_ID'],

        # [required] specify the sheet tab you want to show the result / progress of grading
        'sheet_tab_name': 'main',

        'github_config': {
            # (optional)
            # 'refetch_repo_list': True,

            # (optional)
            # 'clone_repo_mode': 'soft',

            # [required] or (optional)
            # Please setup `use_personal_repo` if repo is not using Github Classroom
            # If using Github Classroom, please comment out `use_personal_repo`
            'use_personal_repo': {
                # specify the range where the personal repo info are. See example at https://docs.google.com/spreadsheets/d/1jZOmd0lkXcllnhtk3DmC7oSM5Q_4H7R-pO9Wy-ydzKo/edit#gid=1501573164
                'sheet_range': 'lab3_personal_repo!B2:Y'
            },

            # (optional) after repo cloned, this code will run in shell environment. Already cd to repo directory for you.
            'repo_additional_command': 'if [ -f ./package.json ]; then npm i; fi'
        },

        # (optional) when grading in interactive console, for each grading, run this code first. Already cd to repo directory for you.
        'grade_additional_command': 'ng serve --open'
    }
