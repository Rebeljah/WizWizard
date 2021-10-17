"""
Module to contain classes for the light control panel located below the
light selection area. The control panel lets the user send commands to the
lights which are selected in the root's light_area using the
LightArea.selected_lights property.
"""

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.slider import Slider
from kivy.uix.button import Button

import backend.light_commands as command


class ControlPanel(GridLayout):
    """
    A control panel to control lights
    """
    def __init__(self, selected_lights: set, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()
        self.selected_lights = selected_lights

        self.cols = 1

        self.brightness_slider = Slider
        self.on_button = Button
        self.dim_button = Button
        self.off_button = Button

        self.build()

    def build(self):
        self.clear_widgets()

        # build brightness slider
        self.brightness_slider = Slider(
            min=0, max=255
        )
        self.brightness_slider.bind(value=lambda _, val: command.command_lights(
                lights=self.selected_lights,
                light_command=command.SetBrightness,
                brightness=val
            )
        )

        # build on/off/dim buttons
        self.on_button = Button(
            text='ON',
            on_release=lambda btn: command.command_lights(
                    lights=self.selected_lights,
                    light_command=command.TurnOnLight
            )
        )
        self.off_button = Button(
            text='OFF',
            on_release=lambda btn: command.command_lights(
                    lights=self.selected_lights,
                    light_command=command.TurnOffLight
            )
        )

        self.dim_button = Button(
            text='DIM',
            on_release=lambda btn: command.command_lights(
                    lights=self.selected_lights,
                    light_command=command.SetBrightness,
                    brightness=1
            )
        )

        # place brightness slider
        self.add_widget(self.brightness_slider)

        # place on/off/dim buttons
        grid = GridLayout(cols=3)
        grid.add_widget(self.on_button)
        grid.add_widget(self.dim_button)
        grid.add_widget(self.off_button)
        self.add_widget(grid)
