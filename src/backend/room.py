from src import backend
from src.backend import utils
from src.observer import Event

from typing import Optional, Union


class Room:
    room_types = (
        'attic', 'balcony', 'bar', 'basement', 'bathroom', 'bedroom', 'corridor',
        'dining', 'dressing', 'entrance', 'garage', 'garden', "kid's room",
        'kitchen', 'living room', 'office', 'playroom', 'terrace', 'tv', 'unassigned'
    )
    _instances = []

    def __init__(self, room_name: str, room_type: str, room_id: Optional[str] = ''):
        Room._instances.append(self)

        self.home = None  # parent
        self.lights = set()  # children

        self.type: str = room_type
        self.name = room_name

        if room_id:
            self._id = room_id
        else:
            self._id = utils.create_uid()

    def __repr__(self):
        return self.name

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

        backend.events.publish(Event.AddedLight, light)

    def remove_light(self, light):
        light.room = None
        self.lights.remove(light)

        backend.events.publish(Event.RemovedLight, light)

    def clear_lights(self):
        for light in self.lights:
            self.remove_light(light)

    @classmethod
    def saved_rooms(cls):
        """Yield rooms that dont subclass TemporaryRoom"""
        for room in cls._instances:
            if not isinstance(room, TemporaryRoom):
                yield room

    @classmethod
    def from_name(cls, name: str, filter_temp_rooms=True) -> Union['Room', None]:
        """looks for an instance of the room in the Room instances list."""
        if filter_temp_rooms:
            rooms = cls.saved_rooms()
        else:
            rooms = cls._instances

        for room in rooms:
            if room.name == name:
                return room
        else:
            raise ValueError(f"No room with name '{name}' ({filter_temp_rooms=})")


class TemporaryRoom(Room):
    """Separate room type for unassigned lights that aren't yet in a room"""
    def __init__(self):
        super().__init__('| New lights |', '', room_id='TEMP_ROOM')
