import pywizlight as pwz

import asyncio as aio
import json
import os


def discover_bulbs():
    """discover lights on LAN and return them"""
    lan_bulbs: list = aio.run(pwz.discovery.discover_lights('192.168.1.255'))
    return lan_bulbs


def save_json(data: dict, filepath, indent: int = 4) -> None:
    folder_path = os.path.join(*os.path.split(filepath)[:-1])
    if not os.path.isdir(folder_path):
        os.mkdir(folder_path)
    with open(filepath, 'w') as outfile:
        json.dump(data, outfile, indent=indent)


def load_json(filepath: str) -> dict:
    with open(filepath) as infile:
        return json.load(infile)
