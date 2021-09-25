from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button

from utils.utils import get_app_and_root

# typing
from models.room import Room


class RoomGrid(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app, self.root = get_app_and_root()
        self.root.add_widget(self)

        self.cols = 7
        self.rows = 1
        self.size_hint_y = 0.2

        self.build()

    def build(self) -> None:
        for room in self.app.home.rooms:
            self.add_widget(self.RoomButton(room))

    class RoomButton(Button):
        def __init__(self, room: Room, **kwargs):
            super().__init__(**kwargs)
            self.app, self.root = get_app_and_root()

            self.room: Room = room
            self.text = room.name
            self.on_release = self.show_room

        def show_room(self):
            self.root.light_pages.current = self.room.id
