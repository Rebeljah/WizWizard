"""A control panel that controls selected lights in a room"""
from tkinter import ttk

import backend


class ControlPanel(ttk.Labelframe):
    def __init__(self, parent):
        super().__init__(parent)
        self.room = None

        self['text'] = 'Control Panel'
        ttk.Button(self).pack()

    def set_room(self, room):
        self.room = room
        self.config(text=room.name)

