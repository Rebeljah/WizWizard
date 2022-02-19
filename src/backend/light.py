"""
Module to contain code for lights and light groups for controlling lights in rooms
"""
import asyncio
from pywizlight.bulb import wizlight as Wizlight
from pywizlight.bulb import PilotBuilder

from . import events
from src.utils.observer import Event

from typing import Optional


class Light:
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
            self._wizlight = None

    @property
    def connected(self) -> bool:
        return isinstance(self._wizlight, Wizlight) and self._wizlight.status

    @property
    def mac(self) -> str:
        return self._mac

    @property
    def brightness(self) -> int:
        """return current brightness 0-255"""
        if self._wizlight:
            return self._wizlight.state.get_brightness()

    @property
    def is_on(self) -> bool:
        """Check if the light is turned on"""
        return self._wizlight and self._wizlight.status

    async def set_wizlight(self, wizlight: Wizlight):
        """Attach a matching bulb to this light. """
        assert wizlight.mac == self._mac
        await wizlight.updateState()
        self._wizlight = wizlight
        events.publish(Event.UpdatedLight, self)

    async def turn_on(self, pilot_builder: PilotBuilder = None):
        if pilot_builder:
            await self._wizlight.turn_on(pilot_builder)
        else:
            await self._wizlight.turn_on()

    async def turn_off(self):
        await self._wizlight.turn_off()
