from backend.light import Light
from backend.utils import create_uid
from backend import events

from typing import Optional as Opt


class Room:
    room_types = (
        'attic', 'balcony', 'bar', 'basement', 'bathroom', 'bedroom', 'corridor',
        'dining', 'dressing', 'entrance', 'garage', 'garden', "kid's room",
        'kitchen', 'living room', 'office', 'playroom', 'terrace', 'tv', 'unassigned'
    )

    def __init__(self, room_name: str, room_type: str, room_id: Opt[str] = ''):
        # parent and children
        self.home = None
        self.lights = set()

        if room_id:
            self._id = room_id
        else:
            self._id = create_uid()

        # room info
        self.type: str = room_type
        self.name = room_name

    @property
    def id(self) -> str:
        """Read-only alias of self._id"""
        return self._id

    def add_light(self, light):
        """Add the light to this room"""
        if light.room:
            light.room.lights.remove(light)
        light.room = self
        self.lights.add(light)
        events.publish('add_light', light)
