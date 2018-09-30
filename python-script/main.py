from interactive import *

if __name__ == '__main__':
    interactive_assignment_setup({
        'mode': 'skip-issue-graded',
        'github_config': {
            'refetch_repo_list': True,
            'clone_repo_mode': 'soft',
            'use_personal_repo': {
                'sheet_range': 'lab2_partb_personal_repo!D1:R'
            },
            'repo_additional_command': 'if [ -f ./package.json ]; then npm i; fi'
        },
        # 'grade_additional_command': 'echo hello'
        'grade_additional_command': 'ng serve --open'
    })