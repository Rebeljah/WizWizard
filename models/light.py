"""
Module to contain code for lights and light groups for controlling lights in rooms
"""
import pywizlight as pwz
from pywizlight import PilotBuilder, PilotParser

import asyncio as aio

Bulb = pwz.wizlight


class Light:
    """Class to represent a light object that controls a real bulb"""
    def __init__(self, name: str, mac: str):
        self.name = name
        self._mac = mac  # read only, use mac property

        self.bulb: Bulb = None  # light will be unavailable if MAC not found on LAN
        self.available = False  #

    @property
    def mac(self) -> str:
        return self._mac

    def set_bulb(self, bulb: Bulb) -> None:
        self.bulb = bulb
        self.available = True

    def toggle(self) -> None:
        aio.run(self.bulb.lightSwitch())

    def set_brightness(self, brightness: int):  # 0-255
        aio.run(self.bulb.turn_on(PilotBuilder(brightness=brightness)))
