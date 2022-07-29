"""A control panel that controls selected lights in a room"""

from tkinter import ttk
from typing import Type

from src import ui
from src.observer import Event
from src.backend.light_commands import (
    command_lights, Lightswitch, SetBrightness, SetLightTemp
)


class ControlPanel(ttk.Labelframe):
    def __init__(self, parent):
        super().__init__(parent)
        self.config(text="Control Panel")
        ui.events.subscribe(Event.SetControlledLights, self.set_controlled_lights)

        self.controlled_lights = set()

        self._build_widgets()

    def _build_widgets(self):
        brightness_frame = ttk.Labelframe(self, text='brightness')
        BrightnessSlider(self, brightness_frame).pack(fill='x')
        brightness_frame.pack(fill='x', padx=40)

        temperature_frame = ttk.Labelframe(self, text='temperature (K)')
        TemperatureSlider(self, temperature_frame).pack(fill='x')
        temperature_frame.pack(fill='x', padx=40)

        # On/Off buttons
        on_off_frame = ttk.Frame(self)
        OnButton(self, on_off_frame).pack(side='left')
        OffButton(self, on_off_frame).pack(side='left')
        on_off_frame.pack()

    def set_controlled_lights(self, lights: set):
        self.controlled_lights = lights

    def command_lights(self, command, **kwargs):
        command_lights(self.controlled_lights, command, **kwargs)


class OnButton(ttk.Button):
    def __init__(self, panel: ControlPanel, parent):
        super().__init__(parent)
        self.panel = panel
        self.config(command=self._on_press)
        self.config(text='On')

    def _on_press(self):
        self.panel.command_lights(Lightswitch, on=True)


class OffButton(ttk.Button):
    def __init__(self, panel: ControlPanel, parent):
        super().__init__(parent)
        self.panel = panel
        self.config(command=self._on_press)
        self.config(text='Off')

    def _on_press(self):
        self.panel.command_lights(Lightswitch, on=False)


class BrightnessSlider(ttk.LabeledScale):
    def __init__(self, panel: ControlPanel, parent):
        super().__init__(parent)
        self.panel = panel
        self.scale.config(command=self._on_value_change)
        self.scale.config(to=255)

    def _on_value_change(self, _):
        self.panel.command_lights(SetBrightness, brightness=self.scale.get())


class TemperatureSlider(ttk.LabeledScale):
    def __init__(self, panel: ControlPanel, parent):
        super().__init__(parent)
        self.panel = panel
        self.scale.config(command=self._on_value_change)
        self.scale.config(from_=1_000, to=10_000)  # Kelvin

    def _on_value_change(self, _):
        self.panel.command_lights(SetLightTemp, temperature=self.scale.get())
