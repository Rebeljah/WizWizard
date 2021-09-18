import json
import os

from typing import Iterable

from light_model import Light


def find_light(lights: Iterable[Light], target_ip: str) -> Light:
    """Find the light with the given IP address, raises ValueError if not found"""
    for light in lights:
        if light.ip == target_ip:
            return light
    else:
        raise ValueError(f"Light with ip {target_ip} not found in lights")


def save_json(data: dict, filepath, indent: int = 4) -> None:
    folderpath = os.path.join(*os.path.split(filepath)[:-1])
    if not os.path.isdir(folderpath):
        os.mkdir(folderpath)
    with open(filepath, 'w') as outfile:
        json.dump(data, outfile, indent=indent)


def load_json(filepath: str) -> dict:
    with open(filepath) as infile:
        return json.load(infile)
