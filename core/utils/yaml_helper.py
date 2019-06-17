from os import path
from glob import glob
from typing import List


def list_files(filepath: str) -> List:
    """ Returns a list of YAML files in a given path.
    :rtype: List
    """
    # check if path exists
    if path.exists(filepath):
        yaml_files = glob(filepath + '*.yaml')
        assert isinstance(yaml_files, List)
        return yaml_files
