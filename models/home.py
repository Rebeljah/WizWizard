
import os

from models.room import Room
from models.light import Light
from utils import utils

# typing
from typing import Iterator, Optional
Rooms = list[Room]
Lights = list[Light]


class Home:
    """
    Represents the root node of the home tree. The Home contain rooms, and rooms
    contains lights.

    :param home_name: The user-visible name of the home
    :param home_id: Unique home-id; created randomly if not passed
    """
    def __init__(self, home_name: str, home_id: Optional[str] = ''):

        self._id = home_id if home_id else utils.create_uid(7)
        self.name = home_name

        self.rooms: Rooms = []
        self.unassigned_lights: Lights = []  # lights not added to home

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
        utils.save_json(data, filepath, indent=4)

    @classmethod
    def from_save(cls, home_id: str):
        """Load then parse home_model data from JSON and return a Home instance"""

        filepath = os.path.join('save_data', f"{home_id}.json")
        home_info = utils.load_json(filepath)
        # get connected bulbs from LAN
        available_bulbs: list = utils.discover_bulbs()

        # create Home
        home = Home(home_info['name'], home_info['id'])

        # add Rooms and Lights to Home
        for room_info in home_info['rooms']:
            # create Room
            room = Room(room_info['name'], room_info['type'], room_info['id'])
            home.add_room(room)

            # add Lights to Room
            for light_info in room_info['lights']:
                light = Light(light_info['name'], light_info['mac'])
                room.add_light(light)

                # assign a bulb from LAN to light
                for bulb in available_bulbs:
                    if bulb.mac == light.mac:
                        available_bulbs.remove(bulb)
                        light.set_bulb(bulb)
                        break

        # add any remaining connected bulbs as unassigned lights to the home
        for i, bulb in enumerate(available_bulbs, 1):
            light = Light(name=f"Unassigned {i}", mac=bulb.mac)
            light.set_bulb(bulb)
            home.unassigned_lights.append(light)

        return home
