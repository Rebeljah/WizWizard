"""
Module to contain code for lights and light groups for controlling lights in rooms
"""
import pywizlight as pwz
from pywizlight import PilotBuilder, PilotParser
import asyncio as aio

from typing import Union, Iterable, Callable
from abc import ABC, abstractmethod

from backend.bulb import Bulb


class Light:
    # TODO add light type names as a class var like the room class
    """Class to represent a light object that controls a real bulb"""
    def __init__(self, name: str, mac: str, bulb: Union[Bulb, None]):
        # parent
        self.room = None

        # light info
        self._mac = mac  # read only, use mac property
        self.name = name

        # bulb that controls a light
        self.connected = False
        if bulb is None:
            self.bulb = bulb
        else:
            self.set_bulb(bulb)

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

    def set_bulb(self, bulb: Bulb) -> None:
        """attach a bulb to this light, the MAC address must match"""
        assert bulb.mac == self._mac
        self.bulb = bulb
        aio.run(self.bulb.updateState())
        self.connected = True
