
import asyncio
from pywizlight import PilotBuilder
from abc import ABC, abstractmethod
from typing import Iterable, Type

from .light import Light


class LightCommand(ABC):
    """A command that can be run asynchronously"""
    def __init__(self, light: Light, **kwargs):
        self.light = light

    @abstractmethod
    async def execute(self):
        """Do async bulb actions"""
        pass


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


def command_lights(lights, command: Type[LightCommand], **kwargs):
    """Build the command for each selected light and run the commands"""
    if not issubclass(command, LightCommand):
        raise TypeError(f'{command} is not a subclass of {LightCommand}')

    commands = build_commands(
        lights=lights, command=command, **kwargs
    )
    run_commands(commands)


def build_commands(lights, command: Type[LightCommand], **kwargs) -> list:
    """Instantiate the given command class with each light. Returns a list of
    commands that are concrete LightCommand instances."""
    return [command(light, **kwargs) for light in lights]


def run_commands(commands: Iterable[LightCommand]):
    for command in commands:
        asyncio.create_task(command.execute())
