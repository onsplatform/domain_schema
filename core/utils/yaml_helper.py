import os
from glob import glob
from typing import List


def list_files(filepath: str) -> List:
    """ Returns a list of YAML files in a given path. """
    if os.path.exists(filepath):
        return glob(filepath + '*.yaml')

def walk_files(target_path):
    """ Returns an iterator of YAML files in a given path. """
    for path, dirs, files in os.walk(target_path):
        yield from [
            os.path.join(path, f) for f in files if f.endswith('.yaml')
        ]
