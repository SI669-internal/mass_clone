import pathlib

DATA_FOLDER_PATH = pathlib.Path(__file__).resolve().parent.parent / 'data'

try:
    from credentials import *
except:
    pass
