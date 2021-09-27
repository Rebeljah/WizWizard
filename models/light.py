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
        self.connected = False  #

    def __hash__(self):
        return hash(self.mac)

    @property
    def mac(self) -> str:
        return self._mac

    @property
    def brightness(self) -> int:
        """return current brightness 0-255"""
        if self.bulb:
            state: PilotParser = aio.run(self.bulb.updateState())
            return state.get_brightness()

    def set_bulb(self, bulb: Bulb) -> None:
        """attach a bulb to this light, the MAC address must match"""
        assert bulb.mac == self.mac
        self.bulb = bulb
        self.connected = True

    def toggle(self) -> None:
        """acts like a lightswitch"""
        aio.run(self.bulb.lightSwitch())

    def set_brightness(self, brightness: int) -> None:
        """Set bulb brightness from 0-255"""
        aio.run(self.bulb.turn_on(PilotBuilder(brightness=brightness)))
