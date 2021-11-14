"""
Module to contain code for lights and light groups for controlling lights in rooms
"""
from pywizlight import wizlight as Wizlight
from pywizlight import PilotParser
import asyncio as aio

from typing import Union


class Light:
    # TODO add light type names as a class var like the room class
    """Class to represent a light object that controls a real bulb"""
    def __init__(self, name: str, mac: str, bulb: Wizlight):
        # parent
        self.room = None

        # light info
        self._mac = mac  # read only, use mac property
        self.name = name

        # bulb controller
        self.bulb: Wizlight = self.set_bulb(bulb)

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

    def set_bulb(self, bulb: Wizlight) -> Wizlight:
        """Attach a matching bulb to this light. """
        assert bulb.mac == self._mac
        aio.run(bulb.updateState())
        self.bulb = bulb
        return self.bulb
