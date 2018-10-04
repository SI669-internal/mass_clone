from utilities import *
from interactive import *

from settings_local import *

if __name__ == '__main__':
    interactive_assignment_setup({
        **get_script_settings(),
        'spreadsheet_id': os.environ['SPREADSHEET_ID'],
    })