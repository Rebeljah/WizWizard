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
import asyncio

import backend.light_commands as command


class ControlPanel(GridLayout):
    """
    A control panel to control lights
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()
        self.root = self.app.root

        self.cols = 1

        self.brightness_slider = Slider
        self.on_button = Button
        self.dim_button = Button
        self.off_button = Button

        self.show_brightness_slider = True

        self.build()

    def build(self):
        self.clear_widgets()

        if self.show_brightness_slider:
            self.brightness_slider = Slider()
            self.add_widget(self.brightness_slider)

        # build on/off/dim buttons
        self.on_button = Button(
            text='ON',
            on_release=lambda btn: self.command_lights(
                command.TurnOnLight)
        )
        self.off_button = Button(
            text='OFF',
            on_release=lambda btn: self.command_lights(
                command.TurnOffLight)
        )

        self.dim_button = Button(
            text='DIM',
            on_release=lambda btn: self.command_lights(
                command.SetBrightness, brightness=1)
        )

        # place on/off/dim buttons
        grid = GridLayout(cols=3)
        grid.add_widget(self.on_button)
        grid.add_widget(self.dim_button)
        grid.add_widget(self.off_button)
        self.add_widget(grid)

    @staticmethod
    def command_lights(light_command, **kwargs):
        """Build the command for each selected light and run the commands"""
        app = App.get_running_app()
        commanded_lights = app.root.light_area.selected_lights

        commands = command.build_commands(
            command=light_command,
            lights=commanded_lights,
            **kwargs
        )
        asyncio.run(command.run_commands(commands))
