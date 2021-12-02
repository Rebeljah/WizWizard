
import asyncio
from pywizlight import PilotBuilder

from backend.light import Light
from utils.limiter import Limiter

from abc import ABC, abstractmethod
from typing import Type
Kelvin = int

LIMITER = Limiter(actions_per_second=9)


class LightCommand(ABC):
    """A command that can be run asynchronously"""
    def __init__(self, light: Light, **kwargs):
        self.light = light

    @abstractmethod
    async def execute(self):
        """Do async wizlight actions"""
        pass


class Lightswitch(LightCommand):
    def __init__(self, light, on=True):
        super().__init__(light)
        self.on = on

    async def execute(self):
        if self.on:
            await self.light.turn_on()
        else:
            await self.light.turn_off()


class SetBrightness(LightCommand):
    """Set light brightness from 0-255"""
    def __init__(self, light, brightness):
        super().__init__(light)

        brightness = int(brightness)
        if not (0 <= brightness <= 255):
            raise ValueError(f'brightness ({brightness}) not in range 0-255')

        self.brightness = brightness

    async def execute(self):
        await self.light.turn_on(
            PilotBuilder(brightness=self.brightness)
        )


class SetLightTemp(LightCommand):
    """Set white light temperature from 0-255"""
    def __init__(self, light, temperature: Kelvin):
        super().__init__(light)

        temperature = int(temperature)
        if not (1_000 <= temperature <= 10_000):
            raise ValueError(f'Invalid temperature: {temperature}K')

        self.temperature: Kelvin = temperature

    async def execute(self):
        await self.light.turn_on(
            PilotBuilder(colortemp=self.temperature)
        )


def command_lights(lights, command: Type[LightCommand], **kwargs):
    """Build the command for each selected light and run the commands"""
    if LIMITER.waiting:
        return  # too soon to run more commands

    if not issubclass(command, LightCommand):
        raise TypeError(f'{command} is not a subclass of {LightCommand}')

    _run_commands(_build_commands(
        lights=lights, command=command, **kwargs
    ))

    LIMITER.wait()


def _build_commands(lights, command: Type[LightCommand], **kwargs) -> list:
    """Instantiate the given command class with each light. Returns a list
    of commands that are concrete LightCommand instances."""
    return [command(light, **kwargs) for light in lights]


def _run_commands(commands):
    for command in commands:
        asyncio.create_task(command.execute())
