import os


def check_path(path):
    os.makedirs(path, exist_ok=True)
