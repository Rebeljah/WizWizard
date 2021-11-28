import os
from pywizlight.discovery import discover_lights

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
        self.unassigned_lights = []

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

        for light in self.unassigned_lights:
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
                bulb = bulbs.get(light.mac, None)
                if bulb:
                    await light.set_bulb(bulb)

        # create lights from any remaining bulbs and add to the unassigned room
        self.unassigned_lights = []
        leftover_bulbs = bulbs.values()
        for i, bulb in enumerate(leftover_bulbs, 1):
            light = Light(name=f"Bulb_{i}", mac=bulb.mac, bulb=bulb)
            self.unassigned_lights.append(light)

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

        filepath = os.path.join('data', f"{self.id}.json")
        utils.save_dict_json(data, filepath, indent=4)

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
