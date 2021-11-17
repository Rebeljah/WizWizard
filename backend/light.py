"""
Module to contain code for lights and light groups for controlling lights in rooms
"""
import asyncio
from pywizlight import wizlight as Wizlight

from . import events


from typing import Optional


class Light:
    # TODO add light type names as a class var like the room class
    """Class to represent a light object that controls a real bulb"""
    def __init__(self, name: str, mac: str, bulb: Optional[Wizlight] = None):
        # parent
        self.room = None

        # light info
        self._mac = mac  # read only, use mac property
        self.name = name

        # set bulb now if it was passed
        if bulb is None:
            self.bulb = None
        else:
            asyncio.create_task(self.set_bulb(bulb))

    @property
    def mac(self) -> str:
        return self._mac

    @property
    def brightness(self) -> int:
        """return current brightness 0-255"""
        if self.bulb:
            return self.bulb.state.get_brightness()

    @property
    def is_on(self) -> bool:
        """Check if the light is turned on"""
        if self.bulb:
            return self.bulb.status
        else:
            return False

    async def set_bulb(self, bulb: Wizlight):
        """Attach a matching bulb to this light. """
        assert bulb.mac == self._mac
        await bulb.updateState()
        self.bulb = bulb
        events.publish('set_bulb', self)
