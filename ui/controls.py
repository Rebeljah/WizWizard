"""A control panel that controls selected lights in a room"""

from tkinter import ttk
from typing import Type

from backend.light import Light
import backend.light_commands as commands
from . import events


class ControlPanel(ttk.Labelframe):
    def __init__(self, parent):
        super().__init__(parent)
        self.config(text="Control Panel")
        events.subscribe('set_controlled_lights', self.set_controlled_lights)

        self.controlled_lights = set()

        # debug
        ttk.Button(self, text='Theme').pack(fill='x', padx=30, pady=3)

        LabeledSlider(self, text='brightness').pack(fill='x', padx=30, pady=3)
        LabeledSlider(self, text='temperature', to=128).pack(fill='x', padx=30, pady=3)

        ttk.Button(self, text='On').pack(fill='x', padx=30, pady=3)
        ttk.Button(self, text='Dim').pack(fill='x', padx=30, pady=3)
        ttk.Button(self, text='Off').pack(fill='x', padx=30, pady=3)

    def set_controlled_lights(self, lights: set):
        self.controlled_lights = lights

    def command_lights(self, command: Type[commands.LightCommand]):
        commands.command_lights(self.controlled_lights, command)


class LabeledSlider(ttk.Labelframe):
    def __init__(self, parent, text, to=255):
        super().__init__(parent, text=text)

        # add slider
        self.scale = ttk.LabeledScale(self, to=to)
        self.scale.pack(fill='both')
