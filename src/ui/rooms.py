"""Code for the displaying tabs of rooms, with lights in each room"""

from tkinter import ttk

from src import ui, backend
from src.ui import utils
from src.utils.observer import Event
from src.backend.room import Room, TemporaryRoom


class RoomTabs(ttk.Notebook):
    """Notebook of tabs, each containing light buttons for a room in the Home"""
    def __init__(self, parent):
        super().__init__(parent)
        self.bind('<<NotebookTabChanged>>', lambda _: self._on_change_tab())
        backend.events.subscribe(Event.AddedRoom, self.add_room_tab)
        backend.events.subscribe(Event.RemovedRoom, self.remove_room_tab)
        ui.events.subscribe(Event.EditedRoom, lambda _: self.update())

        self.selected_lights = set()
        self.new_lights_tab = None

    def _on_change_tab(self):
        curr_tab = self.nametowidget(self.select())
        self.set_selected_lights(curr_tab.selected_lights)

    def set_selected_lights(self, lights):
        self.selected_lights = lights
        ui.events.publish(Event.SetControlledLights, lights)

    def add_room_tab(self, room):
        tab = RoomTab(self, room)
        text = room.name
        if isinstance(room, TemporaryRoom):
            self.add(tab, text=text)
            self.new_lights_tab = tab
        elif self.new_lights_tab in self.winfo_children():
            self.insert(1, tab, text=text)
        else:
            self.add(tab, text=text)

    def remove_room_tab(self, room: Room):
        self.forget(room.name)

        # deselect lights if room lights are selected
        if self.selected_lights.intersection(room.lights):
            self.selected_lights = set()

    def update(self):
        """change tabs titles"""
        for tab in self.tabs():
            room = self.nametowidget(tab).room
            self.tab(tab, text=room.name)


class RoomTab(ttk.Frame):
    """Tab that holds light buttons"""
    def __init__(self, parent, room):
        super().__init__(parent)
        backend.events.subscribe(Event.AddedLight, self.add_light_button)
        self.parent = parent
        self.room = room

        self.selected_lights = set()

    def add_light_button(self, light):
        if light in self.room.lights:
            new_button = LightButton(self, light)
            new_button.pack(side='left', anchor='nw', padx=10, pady=10)

    def select_light(self, light):
        self.selected_lights.add(light)

    def deselect_light(self, light):
        self.selected_lights.remove(light)


class LightButton(ttk.Frame):
    """Frame to hold a light select button and well as display the light name"""
    def __init__(self, room_tab, light):
        super().__init__(room_tab)
        self.tab = room_tab

        LightSelectButton(self, self.tab, light).pack(side='top')
        ttk.Label(self, text=light.name).pack(side='top')


class LightSelectButton(ttk.Button):
    """Button used to select a light."""
    def __init__(self, parent, room_tab, light, **kwargs):
        super().__init__(parent, **kwargs)
        backend.events.subscribe(Event.UpdatedLight, self._update_light)

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

        # check if wizlight is present / on
        if not light.connected:
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
