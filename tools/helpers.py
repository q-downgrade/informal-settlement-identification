import os
from datetime import datetime


def create_directory(directory_folder):
    if not os.path.exists(directory_folder):
        os.makedirs(directory_folder)


def get_current_time():
    return datetime.now().strftime('%Y%m%d_%H%M_%S.%f')
