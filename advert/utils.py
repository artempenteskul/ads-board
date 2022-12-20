import os

from datetime import datetime


def get_timestamp_path(instance, filename):
    return f'{datetime.now().timestamp()}{os.path.splitext(filename)[1]}'
