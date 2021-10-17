"""
Module to contain code for the area where a user can select lights in a
room to control. Buttons that correspond to lights are placed in a grid, and
can be either selected or not selected. Other objects can tell which lights are
selected using the selected_lights attribute of the LightArea.
"""
from kivy.uix.gridlayout import GridLayout
from kivy.uix.togglebutton import ToggleButton
from typing import Iterable

from backend.light import Light


class LightArea(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.rows = 1

        self.lights = []
        self.selected_lights = set()
        self.build()

    def build(self):
        self.clear_widgets()
        for light in self.lights:
            self.add_widget(LightButton(self, light))

    def set_lights(self, lights: Iterable[Light]):
        """Set the lights and add them to selected lights by default"""
        self.lights = list(lights)
        self.build()


class LightButton(ToggleButton):
    def __init__(self, light_area: LightArea, light: Light, **kwargs):
        super().__init__(**kwargs)

        self.light_area = light_area
        self.light = light
        self.text = light.name

        self.bind(state=lambda _, state: self.on_toggle(state))

    def on_toggle(self, state):
        """
        Add or remove self.light from the light_area selected lights on toggle.
        If the light is not connected, the button stays up ('normal').
        """
        if not self.light.is_connected:
            self.state = 'normal'
        elif state == 'down':
            self.light_area.selected_lights.add(self.light)
        elif state == 'normal':
            self.light_area.selected_lights.remove(self.light)
