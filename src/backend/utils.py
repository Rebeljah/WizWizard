
import json
from pathlib import Path
import random
import string

# typing
MAC = str


def save_dict_json(data: dict, path: Path, indent: int = 4) -> None:
    """Save dictionary as JSON to the the filepath"""
    path.parent.mkdir(exist_ok=True)
    with open(path, 'w') as outfile:
        json.dump(data, outfile, indent=indent)


def load_dict_json(path: Path) -> dict:
    """Load json data from the filepath"""
    with open(path) as f:
        return json.load(f)


def create_uid(length: int = 10) -> str:
    """Return a unique alphanumeric identifier string"""
    chars = string.digits + string.ascii_lowercase
    return ''.join(random.sample(chars, length))
