import os
from decouple import config


def open_file():
    os.startfile(config('GAME_PATH'))
