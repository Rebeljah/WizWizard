"""
Module to contain code for lights and light groups for controlling lights in rooms
"""


from pywizlight import wizlight
from pywizlight.exceptions import WizLightTimeOutError
import asyncio as aio

from typing import Iterator


class Light(wizlight):
    def __init__(self, light_name: str, light_ip: str):
        super().__init__(light_ip, connect_on_init=False)
        self.name = light_name
        self._connect()

    def _connect(self):
        try:
            # TODO make this actually async
            aio.run(self.updateState())
        except WizLightTimeOutError:
            # TODO tube_lamp is powered off
            # also, this timeout takes way too long
            raise Warning(f"could not connect light: {self.name}")

    def __repr__(self):
        return f"Light({self.name}, {self.ip})"


class Group:
    """Represents a group of lights that can be controlled together"""
    def __init__(self, name: str):
        self.name = name
        self.lights = []

    @property
    def ips(self) -> Iterator[str]:
        for light in self.lights:
            yield light.ip

    def add_light(self, light):
        self.lights.append(light)
