"""Code for the displaying tabs of rooms, with lights in each room"""

from tkinter import ttk

import backend
from backend.room import Room
from . import utils, events


class RoomTabs(ttk.Notebook):
    """Notebook of tabs, each containing light buttons for a room in the Home"""
    def __init__(self, parent):
        super().__init__(parent)
        self.bind('<<NotebookTabChanged>>', self._on_change_tab)
        backend.events.subscribe('add_room', self.add_room_tab)
        backend.events.subscribe('remove_room', self.remove_room_tab)

        self.selected_lights = set()

    def _on_change_tab(self, event):
        curr_tab = self.nametowidget(self.select())
        self.set_selected_lights(curr_tab.selected_lights)

    def set_selected_lights(self, lights):
        self.selected_lights = lights

        events.publish('set_controlled_lights', lights)

    def add_room_tab(self, room):
        new_tab = RoomTab(self, room)
        self.add(new_tab, text=room.name)

        # check if it is the first tab and set lights
        if not len(self.winfo_children()):
            self.set_selected_lights(new_tab.selected_lights)

    def remove_room_tab(self, room: Room):
        # remove tab
        self.forget(room.name)

        # deselect lights if room lights are selected
        if self.selected_lights.intersection(room.lights):
            self.selected_lights = set()


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
            LightButtonFrame(self, light).pack(side='left', anchor='n')

    def select_light(self, light):
        self.selected_lights.add(light)

    def deselect_light(self, light):
        self.selected_lights.remove(light)


class LightButtonFrame(ttk.Frame):
    """Frame to hold a light select button and well as display the light name"""
    def __init__(self, room_tab, light):
        super().__init__(room_tab)
        self.tab = room_tab

        LightButton(self, self.tab, light).pack(side='top')
        ttk.Label(self, text=light.name).pack(side='top')


class LightButton(ttk.Button):
    """Button used to select a light."""
    def __init__(self, parent, room_tab, light, **kwargs):
        super().__init__(parent, **kwargs)
        backend.events.subscribe('update_light', self._update_light)

        self.tab = room_tab
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
