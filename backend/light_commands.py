from abc import ABC, abstractmethod
from typing import Iterable
import asyncio
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


def command_lights(lights, light_command, **kwargs):
    """Build the command for each selected light and run the commands"""
    commands = build_commands(
        command_class=light_command,
        lights=lights,
        **kwargs
    )
    asyncio.run(run_commands(commands))


def build_commands(command_class, lights, **kwargs) -> list:
    """Instantiate the given command class with each light. Returns a list of
    commands that are concrete LightCommand instances."""
    if not issubclass(command_class, LightCommand):
        raise TypeError(f'{command_class} is not a subclass of {LightCommand}')

    return [command_class(light, **kwargs) for light in lights]


async def run_commands(commands: Iterable[LightCommand]):
    for command in commands:
        await command.execute()
