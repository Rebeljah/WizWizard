"""Code for the displaying tabs of rooms, with lights in each room"""

from tkinter import ttk

import backend
from . import utils


class RoomTabs(ttk.Notebook):
    """Notebook of tabs, each containing light buttons for a room in the Home"""
    def __init__(self, parent):
        super().__init__(parent)
        backend.events.subscribe('add_room', self.add_room_tab)

    def add_room_tab(self, room):
        new_tab = RoomTab(self, room)
        self.add(new_tab, text=room.name)


class RoomTab(ttk.Frame):
    """Tab that holds light buttons"""
    def __init__(self, parent, room):
        super().__init__(parent)
        backend.events.subscribe('add_light', self.add_light_button)
        self.room = room

    def add_light_button(self, light):
        if light in self.room.lights:
            new_button = LightButton(self, light, text=light.name)
            new_button.pack()


class LightButton(ttk.Button):
    """Button used to select a light."""
    def __init__(self, parent, light, **kwargs):
        super().__init__(parent, **kwargs)
        backend.events.subscribe('update_light', self.update_light)
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

    def toggle(self):
        self.selected = not self.selected
        if self.selected:
            self.state(['pressed'])
        else:
            self.state(['!pressed'])

    def update_light(self, light) -> None:
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
