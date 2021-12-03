
import json
import os
import random
import string

# typing
MAC = str


def save_dict_json(data: dict, filepath, indent: int = 4) -> None:
    """Save dictionary as JSON to the the filepath"""
    folder_path = os.path.join(*os.path.split(filepath)[:-1])
    if not os.path.isdir(folder_path):
        os.mkdir(folder_path)
    with open(filepath, 'w') as outfile:
        json.dump(data, outfile, indent=indent)


def load_dict_json(filepath: str) -> dict:
    """Load json data from the filepath"""
    with open(filepath) as infile:
        return json.load(infile)


def create_uid(length: int = 10) -> str:
    """Return a unique alphanumeric identifier string"""
    chars = string.digits + string.ascii_lowercase
    return ''.join(random.sample(chars, length))
