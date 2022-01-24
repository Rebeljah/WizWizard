"""
Module to contain code for lights and light groups for controlling lights in rooms
"""
import asyncio
from pywizlight.bulb import wizlight as Wizlight
from pywizlight.bulb import PilotBuilder

import backend
from . import events


from typing import Optional


class Light:
    # TODO add light type names as a class var like the room class
    """Class to represent a light object that controls a real bulb"""
    def __init__(self, name: str, mac: str, wizlight: Optional[Wizlight] = None):
        # parent
        self.room = None

        # light info
        self._mac = mac  # read only, use mac property
        self.name = name

        # set bulb now if it was passed
        if wizlight:
            asyncio.create_task(self.set_wizlight(wizlight))
        else:
            self.wizlight = None

    @property
    def mac(self) -> str:
        return self._mac

    @property
    def brightness(self) -> int:
        """return current brightness 0-255"""
        if self.wizlight:
            return self.wizlight.state.get_brightness()

    @property
    def is_on(self) -> bool:
        """Check if the light is turned on"""
        return self.wizlight and self.wizlight.status

    async def set_wizlight(self, wizlight: Wizlight):
        """Attach a matching bulb to this light. """
        assert wizlight.mac == self._mac
        await wizlight.updateState()
        self.wizlight = wizlight
        events.publish(backend.LightSetWizlight(light=self))

    async def turn_on(self, pilot_builder: PilotBuilder = None):
        if pilot_builder:
            await self.wizlight.turn_on(pilot_builder)
        else:
            await self.wizlight.turn_on()

    async def turn_off(self):
        await self.wizlight.turn_off()
