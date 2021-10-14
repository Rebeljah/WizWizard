from abc import ABC, abstractmethod
from typing import Iterable, Union
from pywizlight import PilotBuilder

from backend.light import Light


class LightCommand(ABC):
    """A command that can be run asynchronously"""

    def __init__(self, light: Light):
        self.light = light

    @abstractmethod
    async def execute(self):
        """Do async bulb actions"""
        pass


def build_commands(command, lights, **kwargs) -> list:
    return [command(light, **kwargs) for light in lights]


async def run_commands(commands: Iterable[LightCommand]):
    for command in commands:
        await command.execute()


class TurnOnLight(LightCommand):

    def __init__(self, light: Light):
        super().__init__(light)

    async def execute(self):
        await self.light.bulb.turn_on()


class TurnOffLight(LightCommand):

    def __init__(self, light: Light):
        super().__init__(light)

    async def execute(self):
        await self.light.bulb.turn_off()


class SetBrightness(LightCommand):
    """Set light brightness from 0-255"""
    def __init__(self, light, brightness):
        super().__init__(light)

        if not (0 <= brightness <= 255):
            raise ValueError(f'brightness ({brightness}) not in range 0-255')

        self.brightness = brightness

    async def execute(self):
        await self.light.bulb.turn_on(
            PilotBuilder(brightness=self.brightness)
        )
