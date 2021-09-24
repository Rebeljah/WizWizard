from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
# typing
from models.room import Room


class RoomGrid(GridLayout):
    def __init__(self, root, **kwargs):
        assert root.parent is None
        super().__init__(**kwargs)
        root.add_widget(self)

        self.cols = 7
        self.rows = 1
        self.size_hint_y = 0.2

        self.build()

    def build(self) -> None:
        root = self.parent
        for room in root.home_model.rooms:
            self.add_widget(RoomButton(room))


class RoomButton(Button):
    def __init__(self, room: Room, **kwargs):
        super().__init__(**kwargs)

        self.room: Room = room

        self.text = room.name
        self.on_release = self.show_room

    def show_room(self):
        self.parent.parent.set_visible_lights(self.room.lights)
