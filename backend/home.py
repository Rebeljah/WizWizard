
import os
import asyncio as aio

from pywizlight import wizlight as Wizlight
from pywizlight.discovery import discover_lights

from backend.room import Room
from backend.light import Light
from backend import utils

# typing
from typing import Iterator, Optional
Rooms = list[Room]
Lights = list[Light]
MAC = str


class Home:
    """
    Represents the root node of the home tree. The Home contain rooms, and rooms
    contains lights.
    """
    def __init__(self, home_name: str, home_id: Optional[str] = ''):

        self._id = home_id if home_id else utils.create_uid(7)
        self.name = home_name

        self.rooms: Rooms = []
        # room to hold any lights not claimed during loading
        self.unassigned: Room = Room('Unassigned', 'bedroom')

    @property
    def id(self) -> str:
        """Read-only alias of self._id"""
        return self._id

    @property
    def lights(self) -> Iterator[Light]:
        """Gather and return all Lights from rooms in home_model"""
        for room in self.rooms:
            for light in room.lights:
                yield light

    def add_room(self, room: Room) -> None:
        self.rooms.append(room)
        room.home = self

    def save_to_json(self) -> None:
        """Save as JSON the data required to rebuild this Home"""
        data = {
                    "name": self.name,
                    "id": self.id,
                    "rooms": [
                        {
                            "name": room.name,
                            "type": room.type,
                            "id": room.id,
                            "lights": [
                                {
                                    "name": light.name,
                                    "mac": light.mac
                                } for light in room.lights
                            ]
                        } for room in self.rooms
                    ]
                }

        filepath = os.path.join('save_data', f"{self.id}.json")
        utils.save_dict_json(data, filepath, indent=4)

    @classmethod
    def from_save(cls, home_uid: str):
        """Load then parse home_model data from JSON and return a Home instance"""

        filepath = os.path.join('save_data', f"{home_uid}.json")
        home_data = utils.load_dict_json(filepath)

        # get bulb_connected bulbs from LAN
        bulbs: list = aio.run(discover_lights('192.168.1.255'))
        bulbs: dict[MAC, Wizlight] = {bulb.mac: bulb for bulb in bulbs}

        # create Home
        home = Home(home_data['name'], home_data['id'])

        # add Rooms and Lights to Home
        for room_info in home_data['rooms']:
            # create Room
            room = Room(
                room_info['name'], room_info['type'], room_info['id']
            )
            home.add_room(room)

            # add Lights to Room
            for light_info in room_info['lights']:
                mac = light_info['mac']
                name = light_info['name']
                bulb = bulbs.pop(mac, None)
                light = Light(name, mac, bulb)
                room.add_light(light)

        # create lights from any remaining bulbs and add to the unassigned room
        for i, bulb in enumerate(bulbs.values(), 1):
            light = Light(name=f"Bulb_{i}", mac=bulb.mac, bulb=bulb)
            home.unassigned.add_light(light)

        return home
