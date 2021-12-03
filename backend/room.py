
import backend
from backend import utils

from typing import Optional as Opt


class Room:
    room_types = (
        'attic', 'balcony', 'bar', 'basement', 'bathroom', 'bedroom', 'corridor',
        'dining', 'dressing', 'entrance', 'garage', 'garden', "kid's room",
        'kitchen', 'living room', 'office', 'playroom', 'terrace', 'tv'
    )

    def __init__(self, room_name: str, room_type: str, room_id: Opt[str] = ''):
        # parent and children
        self.home = None
        self.lights = set()
        # room info
        self.type: str = room_type
        self.name = room_name

        if room_id:
            self._id = room_id
        else:
            self._id = utils.create_uid()

    @property
    def id(self) -> str:
        """Read-only alias of self._id"""
        return self._id

    def add_light(self, light):
        """Add the light to this room"""
        if light.room:
            light.room.remove_light(light)
        light.room = self
        self.lights.add(light)

        backend.events.publish('add_light', light)

    def remove_light(self, light):
        light.room = None
        self.lights.remove(light)

        backend.events.publish('remove_light', light)

    def clear_lights(self):
        for light in self.lights:
            self.remove_light(light)


class UnassignedRoom(Room):
    """Separate room type for unassigned lights that aren't yet in a room"""
    def __init__(self):
        super().__init__('New lights', '', room_id='unassigned')
