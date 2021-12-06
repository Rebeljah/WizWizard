"""Module to contain code related to menus"""

import tkinter as tk
from tkinter import ttk

from typing import Optional, Type

import backend
import ui
from backend.home import Home
from backend.room import Room
from ui.utils import get_image


class MenuOpener(ttk.Menubutton):
    def __init__(self, parent):
        super().__init__(parent)
        self.config(image=get_image('menu_burger_b'))
        self.config(menu=DropdownMenu(self))


class DropdownMenu(tk.Menu):
    def __init__(self, parent):
        super().__init__(parent, tearoff=0)

        self.add_command(label='Rooms', command=RoomsMenuWindow)
        self.add_command(label='Lights', command=None)


class MenuWindow(tk.Toplevel):
    """Base class for menu modal windows"""
    def __init__(self, title):
        super().__init__()
        self.home: Optional[Home] = backend.active_home
        self.tabs = ttk.Notebook(self)
        self.tabs.pack()
        self.title(title)


class MenuTab(ttk.Frame):
    def __init__(self, parent: Type[MenuWindow]):
        super().__init__(parent)
        self.parent = parent


class RoomsMenuWindow(MenuWindow):
    """Toplevel windows that contains settings dialogs to control Rooms"""
    def __init__(self):
        super().__init__('Rooms')

        for room in self.home.rooms:
            self.tabs.add(RoomSettingsTab(self), text=room.name)

        self.tabs.add(AddRoomTab(self), text='+Add Room')


class RoomSettingsTab(MenuTab):
    """Frame that contains settings dialogs for a room"""
    def __init__(self, parent):
        super().__init__(parent)


class AddRoomTab(MenuTab):
    """Dialog to enter a name and select a type for a new room"""
    def __init__(self, parent):
        super().__init__(parent)

        self.room_name = tk.StringVar()
        self.room_type = tk.StringVar()

        # start building content
        self.content = ttk.Frame(self)

        # build room name input
        self.name_frame = ttk.Labelframe(self.content, text='Room name:')
        ttk.Entry(
            self.name_frame, textvariable=self.room_name
        ).pack()
        self.name_frame.pack(side='top', anchor='w')

        # build type_name input
        self.type_frame = ttk.Labelframe(self.content, text='Room type:')
        ttk.OptionMenu(
            self.type_frame, self.room_type, Room.room_types[0], *Room.room_types
        ).pack()
        self.type_frame.pack(side='top', anchor='w')

        # build submit button
        self.submit_button = ttk.Button(
            self, text='Submit', command=self._submit
        )
        self.submit_button.pack(side='bottom', anchor='se')

        self.content.pack(side='top', padx=50)

    def _submit(self):
        new_room: Room = Room(self.room_name.get(), self.room_type.get())
        ui.events.publish('add_room', new_room)
