
import os
import json

from room_model import Room
from light_model import Light, Group
import utils

from typing import Iterator
Rooms = list[Room]


class Home:
    def __init__(self, home_name: str, home_id: str):
        self._id = home_id  # read only
        self.name = home_name
        self.rooms: Rooms = []

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
                            "id": room.id,
                            "lights": [
                                {
                                    "name": light.name,
                                    "ip": light.ip
                                } for light in room.lights
                            ],
                            "groups": [
                                {
                                    "name": group.name,
                                    "ips": group.ips
                                } for group in room.groups
                            ]
                        } for room in self.rooms
                    ]
                }
        filepath = os.path.join('', 'homes', f"{self.id}.json")
        utils.save_json(data, filepath, indent=4)

    @classmethod
    def from_save(cls, home_id: str):
        """Load then parse home_model data from JSON and return a Home instance"""
        filepath = os.path.join('', 'homes', f"{home_id}.json")
        home_info = utils.load_json(filepath)

        # create Home
        home = Home(home_info['name'], home_info['id'])

        # add Rooms and Lights to Home
        for room_info in home_info['rooms']:
            # create Room
            room = Room(room_info['name'], room_info['id'])
            home.add_room(room)

            # add Lights to Room
            for light_info in room_info['lights']:
                light = Light(light_info['name'], light_info['ip'])
                room.add_light(light)

            # add Groups using the loaded lights
            for group_info in room_info['groups']:
                # add Group to Home
                group = Group(group_info['name'])
                room.add_group(group)
                # add lights to group
                for ip in group_info['ips']:
                    light = utils.find_light(home.lights, ip)
                    group.add_light(light)
        return home
