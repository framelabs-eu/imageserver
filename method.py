import os
import random

from imageprepare import prepare_file


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
            return (404, f'No files at \'{path}\''.encode())
        random.shuffle(files)
        for filename in files:
            filepath = os.path.join(root, filename)
            content = get_content(filepath, config)
            if content:
                print(f'Serving {filename}')
                return (200, content)
    return (404, f'No servable files at \'{path}\''.encode())
