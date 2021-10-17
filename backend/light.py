"""
Module to contain code for lights and light groups for controlling lights in rooms
"""
from pywizlight import PilotParser
import asyncio as aio

from typing import Union

from backend.bulb import Bulb


class Light:
    # TODO add light type names as a class var like the room class
    """Class to represent a light object that controls a real bulb"""
    def __init__(self, name: str, mac: str):
        # parent
        self.room = None

        # light info
        self._mac = mac  # read only, use mac property
        self.name = name
        self.bulb = None
        self.is_connected = False  # established when bulb is set

    @property
    def mac(self) -> str:
        return self._mac

    @property
    def brightness(self) -> int:
        """return current brightness 0-255"""
        if self.bulb:
            state: PilotParser = aio.run(self.bulb.updateState())
            return state.get_brightness()

    @property
    def is_on(self) -> bool:
        """Check if the light is turned on"""
        return self.bulb.status

    async def set_bulb(self, bulb: Bulb) -> None:
        """attach a bulb to this light, the MAC address must match"""
        assert bulb.mac == self._mac
        await bulb.updateState()
        self.bulb = bulb
        self.is_connected = True
