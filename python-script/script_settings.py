import pathlib

DATA_FOLDER_PATH = pathlib.Path.cwd() / '..' / 'data'

try:
    from credentials import *
except:
    pass
