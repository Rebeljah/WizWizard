"""Code for the displaying tabs of rooms, with lights in each room"""

from tkinter import ttk
from typing import Iterator

import backend
from . import utils, events


class RoomTabs(ttk.Notebook):
    """Notebook of tabs, each containing light buttons for a room in the Home"""
    def __init__(self, parent):
        super().__init__(parent)
        self.bind('<<NotebookTabChanged>>', self._on_change_tab)
        backend.events.subscribe('add_room', self.add_room_tab)

        self.selected_lights = set()

    def _on_change_tab(self, event):
        curr_tab = self.nametowidget(self.select())
        self.set_selected_lights(curr_tab.selected_lights)

    def set_selected_lights(self, lights):
        self.selected_lights = lights
        events.publish('set_controlled_lights', lights)

    def add_room_tab(self, room):
        # check if it is the first tab and set lights
        if len(self.winfo_children()) == 0:
            self.set_selected_lights(room.lights)

        new_tab = RoomTab(self, room)
        self.add(new_tab, text=room.name)


class RoomTab(ttk.Frame):
    """Tab that holds light buttons"""
    def __init__(self, parent, room):
        super().__init__(parent)
        backend.events.subscribe('add_light', self.add_light_button)
        self.parent = parent
        self.room = room

        self.selected_lights = set()

    def add_light_button(self, light):
        if light in self.room.lights:
            new_button = LightButton(self, light, text=light.name)
            new_button.pack(side='left', anchor='nw', padx=10, pady=10)

    def select_light(self, light):
        self.selected_lights.add(light)

    def deselect_light(self, light):
        self.selected_lights.remove(light)


class LightButton(ttk.Button):
    """Button used to select a light."""
    def __init__(self, parent, light, **kwargs):
        super().__init__(parent, **kwargs)
        backend.events.subscribe('update_light', self._update_light)

        self.tab = parent
        self.light = light

        # Toggle behavior
        self.selected = False
        self.config(command=self.toggle)

        self.images = {
            'w': {
                'off': utils.get_image('lightbulb-off_w'),
                'on': utils.get_image('lightbulb-on_w'),
                'alert': utils.get_image('lightbulb-alert_w')
            }
        }

        self.image_state = 'alert'
        self._update_image()

    def _update_image(self) -> None:
        self.config(image=self.images['w'][self.image_state])

    def _update_light(self, light) -> None:
        if light is not self.light:
            return

        # check if bulb is present / on
        if not light.bulb:
            self.image_state = 'alert'
        elif light.is_on:
            self.image_state = 'on'
        else:
            self.image_state = 'off'

        self._update_image()

    def toggle(self):
        self.selected = not self.selected
        if self.selected:
            self.state(['pressed'])
            self.tab.select_light(self.light)
        else:
            self.state(['!pressed'])
            self.tab.deselect_light(self.light)
