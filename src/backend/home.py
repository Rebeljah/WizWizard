from pathlib import Path
from functools import partial
from tkinter.simpledialog import askstring
from pywizlight.discovery import discover_lights

from src.observer import Event
from src import ui, backend
from src.backend import utils
from src.backend.room import Room, TemporaryRoom
from src.backend.light import Light


from typing import Iterator, Optional
RoomId = MAC = str

HOME_DATA_PATH = Path(__file__).parent.parent.parent / 'data' / 'homes'


class Home:
    """
    Represents the root node of the home tree. The Home contain rooms, and rooms
    contains lights.
    """
    active_home = None

    def __init__(self, home_name: str, home_id: Optional[str] = ''):
        self._id = home_id or utils.create_uid()
        self.name = home_name
        self.rooms = []

        ui.events.subscribe(Event.AddedRoom, partial(self.add_room, save=True))
        ui.events.subscribe(Event.EditedRoom, lambda _: self.save_to_json())

        # this lets the app reload the home on restart.
        self._set_as_last_loaded()

    def _set_as_last_loaded(self):
        with open(HOME_DATA_PATH / 'last_loaded.txt', 'w') as f:
            f.write(self.id)

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

    def add_room(self, room: Room, save=False) -> None:
        """Add the room to the home"""
        self.rooms.append(room)
        room.home = self

        backend.events.publish(Event.AddedRoom, room)
        if save:
            self.save_to_json()

    def remove_room(self, room: Room, save=False) -> None:
        """Remove the room given room"""
        self.rooms.remove(room)

        backend.events.publish(Event.RemovedRoom, room)
        if save:
            self.save_to_json()

    async def find_lights(self):
        """Find wizlights and attach them to lights. Add any unassigned lights"""
        found_lights = {}
        for wizlight in await discover_lights('192.168.1.255'):
            found_lights[wizlight.mac] = wizlight

        # pop and attach wizlights to lights with matching MACs
        for light in self.lights:
            if wiz_l := found_lights.pop(light.mac, False):
                await light.set_wizlight(wiz_l)

        # Check if there are any unassigned wizlights left
        if not (remaining := found_lights.values()):
            return

        # Re-instantiate the home's new lights room
        new_lights_room = TemporaryRoom()
        self.add_room(new_lights_room)

        # add any remaining wizlights to unassigned room
        for wizlight in remaining:
            new_lights_room.add_light(
                Light(name=wizlight.mac, mac=wizlight.mac, wizlight=wizlight)
            )

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
                } for room in Room.saved_rooms()
            ]
        }

        filepath = HOME_DATA_PATH / f'{self.id}.json'
        utils.save_dict_json(data, filepath)

    @classmethod
    def from_save(cls, home_uid: str):
        """Load then parse home_model data from JSON and return a Home instance"""

        filepath = HOME_DATA_PATH / f'{home_uid}.json'
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

        cls.active_home = home
        return home

    @classmethod
    def get_last_loaded(cls):
        save_path = HOME_DATA_PATH / 'last_loaded.txt'

        with open(save_path, 'a+') as f:
            f.seek(0)
            home_uid = f.read()

        if home_uid:
            return Home.from_save(home_uid)
        else:
            return Home.make_new_home()
    
    @classmethod
    def make_new_home(cls):
        new_home_name = askstring('New home', 'Home name')
        
        if new_home_name == '':
            return

        new_home = Home(new_home_name)
        new_home.save_to_json()
        
        return new_home
