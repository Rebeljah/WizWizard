import os
from pywizlight.discovery import discover_lights

import backend
from backend import utils
from backend.room import Room, UnassignedRoom
from backend.light import Light


from typing import Iterator, Optional
RoomId = MAC = str


class Home:
    """
    Represents the root node of the home tree. The Home contain rooms, and rooms
    contains lights.
    """
    def __init__(self, home_name: str, home_id: Optional[str] = ''):
        self._id = home_id or utils.create_uid()
        self.name = home_name
        self.rooms: set = set()

    @property
    def id(self) -> str:
        """Read-only alias of self._id"""
        return self._id

    @property
    def saved_rooms(self) -> Iterator[Room]:
        """Yield rooms that should be saved to the data folder"""
        for room in self.rooms:
            if not isinstance(room, UnassignedRoom):
                yield room

    @property
    def lights(self) -> Iterator[Light]:
        """Iterate over lights in the home"""
        for room in self.rooms:
            for light in room.lights:
                yield light

    def add_room(self, room: Room) -> None:
        """Add the room to the home"""
        self.rooms.add(room)
        room.home = self
        backend.events.publish('home_add_room', room)

    def remove_room(self, room: Room):
        """Remove the room given room"""
        self.rooms.remove(room)
        backend.events.publish('home_remove_room', room)

    async def find_lights(self):
        """Find wizlights and attach them to lights. Add any unassigned lights"""
        found_lights = {}
        for wizlight in await discover_lights('192.168.1.255'):
            found_lights[wizlight.mac] = wizlight

        # pop and attach wizlights to lights with matching MACs
        for light in self.lights:
            if b := found_lights.pop(light.mac, False):
                await light.set_wizlight(b)

        # return if no wizlights are remaining
        if not (remaining := found_lights.values()):
            return

        # Re-instantiate the unassigned lights room
        room = UnassignedRoom()
        self.add_room(room)

        # add any remaining wizlights to unassigned room
        for wizlight in remaining:
            room.add_light(
                Light(name=wizlight.ip, mac=wizlight.mac, wizlight=wizlight)
            )

    def save(self) -> None:
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
                } for room in self.saved_rooms
            ]
        }

        utils.save_dict_json(data, os.path.join('data', f"{self.id}.json"))

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
