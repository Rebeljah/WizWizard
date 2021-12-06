import os
from pywizlight.discovery import discover_lights

import backend
import ui
from . import utils, events
from .room import Room
from .light import Light


from typing import Iterator, Optional
MAC = str


class Home:
    """
    Represents the root node of the home tree. The Home contain rooms, and rooms
    contains lights.
    """
    def __init__(self, home_name: str, home_id: Optional[str] = ''):
        self._id = home_id if home_id else utils.create_uid(7)
        self.name = home_name

        self.rooms = []
        self.unassigned_room = Room('', '', '')

        backend.active_home = self
        ui.events.subscribe('add_room', self.add_room, self.on_edit_home)

    @property
    def id(self) -> str:
        """Read-only alias of self._id"""
        return self._id

    @property
    def lights(self) -> Iterator[Light]:
        """Iterate over lights in the home"""
        for room in self.rooms:
            for light in room.lights:
                yield light

    def add_room(self, room: Room) -> None:
        self.rooms.append(room)
        room.home = self
        events.publish('add_room', room)

    async def update_lights(self):
        """Find bulbs and attach them to lights"""
        # get bulb_connected bulbs from LAN
        bulbs = await discover_lights('192.168.1.255')
        bulbs = {bulb.mac: bulb for bulb in bulbs}

        for room in self.rooms:
            for light in room.lights:
                bulb = bulbs.pop(light.mac, None)
                if bulb:
                    await light.set_bulb(bulb)

        # create lights from any remaining bulbs and add to the unassigned room
        if self.rooms[-1].type == 'unassigned':
            del self.rooms[-1]

        self.unassigned_room = Room('New bulbs', room_type='unassigned')
        self.add_room(self.unassigned_room)

        for bulb in bulbs.values():
            light = Light(name=bulb.ip, mac=bulb.mac, bulb=bulb)
            self.unassigned_room.add_light(light)

    def on_edit_home(self, *args):
        self.save_to_json()

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
                        } for room in self.rooms if room.type != 'unassigned'
                    ]
                }

        filepath = os.path.join('data', 'homes', f"{self.id}.json")
        utils.save_dict_json(data, filepath)

    @classmethod
    def from_save(cls, home_uid: str):
        """Load then parse home_model data from JSON and return a Home instance"""

        filepath = os.path.join('data', 'homes', f"{home_uid}.json")
        home_data = utils.load_dict_json(filepath)

        # create Home
        home = cls(home_data['name'], home_data['id'])

        # add Rooms and Lights to Home
        for room_data in home_data['rooms']:
            # create Room
            room = Room(
                room_data['name'], room_data['type'], room_data['id']
            )
            home.add_room(room)

            # add Lights to Room
            for light_data in room_data['lights']:
                light = Light(light_data['name'], light_data['mac'])
                room.add_light(light)

        return home
