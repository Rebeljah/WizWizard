
import pywizlight as pwz
from pywizlight.discovery import find_wizlights
import json
import os
import random
import string

from backend.bulb import Bulb

# typing
MAC = str


async def discover_bulbs(broadcast_space="255.255.255.255") -> dict[MAC, Bulb]:
    """Find lights and return dict with Bulb objects."""
    registry_bulbs = await find_wizlights(broadcast_address=broadcast_space)

    # empty list for adding bulbs
    bulbs = []
    for new_bulb in registry_bulbs:
        try:
            bulb = Bulb(ip=new_bulb.ip_address, mac=new_bulb.mac_address)
            bulbs.append(bulb)
        except pwz.exceptions.WizLightTimeOutError as e:
            raise Warning(
                f'{e}: connection timed out for bulb with MAC {new_bulb.mac_address}'
            )

    return {bulb.mac: bulb for bulb in bulbs}


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


def create_uid(length: int = 7) -> str:
    """Return a unique identifier containing digits 0-9"""
    return ''.join(random.sample(string.digits, length))
