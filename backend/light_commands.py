
import asyncio
import time

from pywizlight import PilotBuilder

from abc import ABC, abstractmethod
from typing import Iterable, Type

from .light import Light

Kelvin = int


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

        brightness = int(brightness)
        if not (0 <= brightness <= 255):
            raise ValueError(f'brightness ({brightness}) not in range 0-255')

        self.brightness = brightness

    async def execute(self):
        await self.light.bulb.turn_on(
            PilotBuilder(brightness=self.brightness)
        )


class SetTemperature(LightCommand):
    """Set light brightness from 0-255"""
    def __init__(self, light, temperature: Kelvin):
        super().__init__(light)

        temperature = int(temperature)
        if not (1000 <= temperature <= 10000):
            raise ValueError(f'Invalid temperature: {temperature}K')

        self.temperature: Kelvin = temperature

    async def execute(self):
        await self.light.bulb.turn_on(
            PilotBuilder(colortemp=self.temperature)
        )


class LightCommander:
    def __init__(self, commands_per_second):
        """Class to build and run commands. Commands are limited to a certain
        number of batches per second"""
        self.last_action_time = 0.0
        self.wait_time = 1 / commands_per_second

    def command_lights(self, lights, command: Type[LightCommand], **kwargs):
        """Build the command for each selected light and run the commands"""
        elapsed_time = time.perf_counter() - self.last_action_time
        if elapsed_time < self.wait_time:
            return  # too soon to run more commands

        if not issubclass(command, LightCommand):
            raise TypeError(f'{command} is not a subclass of {LightCommand}')

        commands = self._build_commands(
            lights=lights, command=command, **kwargs
        )
        self._run_commands(commands)

        self.last_action_time = time.perf_counter()

    @staticmethod
    def _build_commands(lights, command: Type[LightCommand], **kwargs) -> list:
        """Instantiate the given command class with each light. Returns a list
        of commands that are concrete LightCommand instances."""
        return [command(light, **kwargs) for light in lights]

    @staticmethod
    def _run_commands(commands):
        for command in commands:
            asyncio.create_task(command.execute())
