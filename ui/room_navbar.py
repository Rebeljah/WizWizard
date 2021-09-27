from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button

from utils.utils import get_app_and_root

# typing
from models.room import Room


class RoomNavbar(GridLayout):
    """Grid layout to hold room buttons"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app, self.root = get_app_and_root()

        self.build()

    def build(self) -> None:
        self.cols = 7
        self.rows = 1
        self.size_hint_y = 0.2
        self.padding = 15

        for room in self.app.home.rooms:
            self.add_widget(RoomNavButton(room.name, room.id))


class RoomNavButton(Button):
    """A button for selecting the room to control lights in"""
    def __init__(self, room_name: str, room_id: str, **kwargs):
        super().__init__(**kwargs)
        self.app, self.root = get_app_and_root()

        # store the room name and id
        self.room_name = room_name
        self.room_id: str = room_id

        # button formatting
        self.text = self.room_name
        self.on_release = self.show_room

    def show_room(self):
        """Set room controls page to this room using the room id"""
        screen_manager = self.root.room_controls
        screen_manager.current = self.room_id
