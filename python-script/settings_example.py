'''
    This File Serve As Script Setting Template Only

    PLEASE DO FOLLOWING BEFORE RUNNING THE SCRIPT:

    1. Copy this file and rename as settings_local.py
    2. Modify the parameters in get_script_settings() based on the API below & your needs

'''

'''

CONFIGURABLE PARAMETERS

[required] sheet_tab_name
Specifies the sheet tab you want to show the result / progress of grading. e.g. "main".
Using the spreadsheet specified in `os.environ['SPREADSHEET_ID']` in `credentials.py`.

(optional) skip-mode
Available options listed below.
'skip-issue-graded': skip commented submits and graded submits.
'skip-issue': skip commented submits
'default' or '': always ask before skip

(optional) repo_additional_command
After repo cloned, this code will run in shell environment. Already cd to repo directory for you.
e.g. to install npm packages right after clone, write 'if [ -f ./package.json ]; then npm i; fi'

(optional) grade_additional_command
When grading in interactive console, for each grading, run this code first. Already cd to repo directory for you.
e.g. run Angular app before grading by writing 'ng serve --open'
If you don't specify this key, by default will open vscode for you by running `code .`

(optional) refetch_repo_list=False
True: always refetch repo list from Github API or spreadsheet
False: use existing repo url in cache; only fetch online if not exist in local cache

(optional) clone_repo_mode='soft'
'soft': only clone repo if not exist in local
'hard': wipe local repos and re-clone all (only for the given assignment prefix)

(optional) use_personal_repo
If students use personal repo url instead of Github Classroom, specifies this key.
Otherwise if students are using Github Classroom, do not specify this key or please comment out the whole key - value pair.

    [required if key `use_personal_repo` specified] sheet_range
    The range in sheet providing personal repo urls, format is
    '<sheet tab name>!<range>', e.g. 'lab3_personal_repo!B2:Y'.
    Make sure the first row in the range gives the repo names (without .git),
    the second row gives students' github account name,
    the third row gives students' full name.
    See example at https://docs.google.com/spreadsheets/d/1jZOmd0lkXcllnhtk3DmC7oSM5Q_4H7R-pO9Wy-ydzKo/edit#gid=1501573164


'''

def get_script_settings():
    return {
        # (optional) available options listed below.
        #     'skip-issue-graded': skip commented submits and graded submits.
        #     'skip-issue': skip commented submits
        #     'default': always ask before skip
        'skip-mode': 'default',
        "is_batch_processing": False,


        # [required] specify the sheet tab you want to show the result / progress of grading  
        'sheet_tab_name': 'main',
        'sheet_tab_ranges': {
            'overall': 'A3:AH',
            'roster': {
                'start_row_index': {
                    'student_full_names': 2,
                    'github_accounts': 1,
                    'uniqnames': 0,
                },
                'start_column_index': 3,
            },
            'data': {
                'start_row_index': 3,
                'start_column_index': 0,
            } 
        },


        'github_config': {
            # (optional)
            'refetch_repo_list': False,

            # (optional)
            'clone_repo_mode': 'hard',

            # # [required] only if repo is not using Github Classroom; otherwise, please comment out.
            # 'use_personal_repo': {
            #     # specify the range where the personal repo info are. See example at https://docs.google.com/spreadsheets/d/1jZOmd0lkXcllnhtk3DmC7oSM5Q_4H7R-pO9Wy-ydzKo/edit#gid=1501573164
            #     'sheet_range': 'lab3_personal_repo!B2:Y'
            # },

            # (optional) after repo cloned, this code will run in shell environment. Already cd to repo directory for you.
            # 'repo_additional_command': 'if [ -f ./package.json ]; then npm i; fi'
        },


        # (optional) when grading in interactive console, for each grading, will run this code first. Already cd to repo directory for you.
        # 'ng serve --open'
        # 'ionic serve --platform ios'

        "grade_additional_command": "open -a Visual\ Studio\ Code .",
    }
