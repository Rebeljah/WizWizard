"""Code for the displaying tabs of rooms, with lights in each room"""

from tkinter import ttk

import backend


class RoomTabs(ttk.Notebook):
    def __init__(self, parent):
        super().__init__(parent)
        backend.events.subscribe('add_room', self.add_room_tab)

    def add_room_tab(self, room):
        new_tab = RoomTab(self, room)
        self.add(new_tab, text=room.name)


class RoomTab(ttk.Frame):
    def __init__(self, parent, room):
        super().__init__(parent)
        self.room = room
        backend.events.subscribe('add_light', self.add_light_button)

    def add_light_button(self, light):
        if light in self.room.lights:
            new_button = LightButton(self, light, text=light.name)
            new_button.pack()


class LightButton(ttk.Button):
    def __init__(self, parent, light, **kwargs):
        super().__init__(parent, **kwargs)
        self.light = light
        backend.events.subscribe('update_light', self.update_light)

    def update_light(self, light):
        pass
