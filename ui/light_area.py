"""
Module to contain code for the area where a user can select lights in a
room to control. Buttons that correspond to lights are placed in a grid, and
can be either selected or not selected. Lights that are selected can be controlled
in the light control panel using the selected_lights property
"""
from kivy.uix.gridlayout import GridLayout
from kivy.uix.togglebutton import ToggleButton
from typing import Union, Iterator

from backend.light import Light
from backend.room import Room

Lights = Union[tuple[Light], list[Light]]


class LightArea(GridLayout):
    def __init__(self, room: Room = None, **kwargs):
        super().__init__(**kwargs)

        self.rows = 1

        self.room = room
        if self.room is not None:
            self.set_room(self.room)

    def build(self):
        self.clear_widgets()
        for light in self.room.lights:
            self.add_widget(LightButton(light))

    @property
    def selected_lights(self) -> Iterator[Light]:
        """Yield the light of each selected button"""
        light_btn: LightButton
        for light_btn in self.children:
            if light_btn.state == 'down':
                yield light_btn.light

    def set_room(self, room: Room):
        if room is not self.room:
            self.room = room
            self.build()


class LightButton(ToggleButton):
    def __init__(self, light: Light, **kwargs):
        super().__init__(**kwargs)

        self.light = light
        self.text = light.name
