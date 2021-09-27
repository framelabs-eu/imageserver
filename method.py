import os
import random

from imageprepare import prepare_file
from pathlib import Path


def get_content(filepath, config):
    try:
        rawz = prepare_file(filepath, config)
        return rawz
    except Exception:
        print(f'File \'{filepath}\' is not supported')
        return None

def random_file_content(path, config):
    for root, _, files in os.walk(path):
        # print(files)
        if not len(files):
            return (404, None, f'No files at \'{path}\''.encode())
        random.shuffle(files)
        for filename in files:
            filepath = os.path.join(root, filename)
            content = get_content(filepath, config)
            if content:
                print(f'Serving {filename}')
                filename = Path(filename).stem # remove file extension
                return (200, filename, content)
    return (404, None, f'No servable files at \'{path}\''.encode())
