from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown

from functools import partial

from backend.room import Room
from ui import forms


class Navbar(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.rows = 1
        self.size_hint_y = 0.2
        self.padding = 10

        self.build()

    def build(self):
        self.clear_widgets()

        app = App.get_running_app()
        rooms: list[Room] = app.home.rooms[:]
        unassigned_room = app.home.unassigned
        if len(unassigned_room.lights):
            rooms.append(app.home.unassigned)

        for room in rooms:
            self.add_widget(Button(
                text=room.name,
                on_release=partial(
                    lambda lights, btn: app.root.set_shown_lights(lights),
                    room.lights
                )
            ))

        # Build dropdown to hold add item buttons
        dropdown = DropDown()
        self.add_widget(Button(
            text='Menu',
            on_release=lambda btn: dropdown.open(btn)
        ))
        dropdown.add_widget(Button(
            size_hint_y=None,
            height=44,
            text='+ Room',
            on_release=lambda btn: forms.AddRoomForm().open()
        ))
        dropdown.add_widget(Button(
            size_hint_y=None,
            height=44,
            text='+ Light',
            on_release=lambda btn: forms.AddLightForm().open()
        ))
