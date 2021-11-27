"""A control panel that controls selected lights in a room"""

from tkinter import colorchooser
from tkinter import ttk
from typing import Type
from abc import ABC, abstractmethod

from backend.light_commands import (
    command_lights, TurnOnLight, TurnOffLight, SetBrightness, SetTemperature
)
from . import events


class ControlPanel(ttk.Labelframe):
    def __init__(self, parent):
        super().__init__(parent)
        self.config(text="Control Panel")
        events.subscribe('set_controlled_lights', self.set_controlled_lights)

        self.controlled_lights = set()
        self._build_widgets()

    def _build_widgets(self):
        brightness_frame = ttk.Labelframe(self, text='brightness')
        BrightnessSlider(self, brightness_frame).pack(fill='x')
        brightness_frame.pack(fill='x', padx=40)

        temperature_frame = ttk.Labelframe(self, text='temeperature (K)')
        TemperatureSlider(self, temperature_frame).pack(fill='x')
        temperature_frame.pack(fill='x', padx=40)

        # On/Off buttons
        on_off_frame = ttk.Frame(self)
        OnButton(self, on_off_frame).pack(side='left')
        OffButton(self, on_off_frame).pack(side='left')
        on_off_frame.pack()

    def set_controlled_lights(self, lights: set):
        self.controlled_lights = lights


class OnButton(ttk.Button):
    def __init__(self, panel: ControlPanel, parent):
        super().__init__(parent)
        self.panel = panel
        self.config(command=self._on_press)
        self.config(text='On')

    def _on_press(self):
        lights = self.panel.controlled_lights
        command_lights(lights, TurnOnLight)


class OffButton(ttk.Button):
    def __init__(self, panel: ControlPanel, parent):
        super().__init__(parent)
        self.panel = panel
        self.config(command=self._on_press)
        self.config(text='Off')

    def _on_press(self):
        lights = self.panel.controlled_lights
        command_lights(lights, TurnOffLight)


class BrightnessSlider(ttk.Scale):
    def __init__(self, panel: ControlPanel, parent):
        super().__init__(parent)
        self.panel = panel
        self.config(command=self._on_value_change)
        self.config(to=255)

    def _on_value_change(self, _):
        lights = self.panel.controlled_lights
        command_lights(lights, SetBrightness, brightness=self.get())


class TemperatureSlider(ttk.Scale):
    def __init__(self, panel: ControlPanel, parent):
        super().__init__(parent)
        self.panel = panel
        self.config(command=self._on_value_change)
        self.config(from_=1_000, to=10_000)  # Kelvin

    def _on_value_change(self, _):
        lights = self.panel.controlled_lights
        command_lights(lights, SetTemperature, temperature=self.get())
