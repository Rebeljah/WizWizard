"""Module to contain code related to menus"""

import tkinter as tk
from tkinter import ttk

from typing import Optional, Type
from abc import ABC, abstractmethod

import backend
import ui
from backend.home import Home
from backend.room import Room
from ui.utils import get_image


class MenuOpener(ttk.Menubutton):
    def __init__(self, parent):
        super().__init__(parent)
        self.config(image=get_image('menu_burger_b'))

        self.menu = tk.Menu(self, tearoff=0)
        self.config(menu=self.menu)
        self.menu.add_command(label='Rooms', command=RoomsMenuWindow)
        self.menu.add_command(label='Lights', command=LightsMenuWindow)


class MenuWindow(tk.Toplevel, ABC):
    """Base class for menu modal windows"""
    def __init__(self, title):
        super().__init__()
        self.title(title)
        self.home: Optional[Home] = backend.active_home
        self.tabs = ttk.Notebook(self)

    @abstractmethod
    def _build_tabs(self):
        pass


class RoomsMenuWindow(MenuWindow):
    """Toplevel windows that contains settings dialogs to control Rooms"""
    def __init__(self):
        super().__init__('Rooms')
        self._build_tabs()

    def _build_tabs(self):
        for room in self.home.rooms:
            self.tabs.add(RoomSettingsTab(self), text=room.name)
        self.tabs.add(CreateRoomTab(self), text='+Add Room')

        self.tabs.pack()


class RoomSettingsTab(ttk.Frame):
    """Frame that contains settings dialogs for a room"""
    def __init__(self, parent):
        super().__init__(parent)


class CreateRoomTab(ttk.Frame):
    """Dialog to enter a name and select a type for a new room"""
    def __init__(self, parent):
        super().__init__(parent)

        self.room_name = tk.StringVar()
        self.room_type = tk.StringVar()

        # start building content
        self.form_content = ttk.Frame(self)

        # build room name input
        self.name_frame = ttk.Labelframe(self.form_content, text='Room name:')
        ttk.Entry(
            self.name_frame, textvariable=self.room_name
        ).pack()
        self.name_frame.pack(side='top', anchor='w')

        # build type_name input
        self.type_frame = ttk.Labelframe(self.form_content, text='Room type:')
        ttk.OptionMenu(
            self.type_frame, self.room_type, Room.room_types[0], *Room.room_types
        ).pack()
        self.type_frame.pack(side='top', anchor='w')

        self.form_content.pack(side='top', padx=50)

        # build submit button
        self.submit_button = ttk.Button(
            self, text='Submit', command=self._submit
        )
        self.submit_button.pack(side='bottom', anchor='se')

    def _submit(self):
        name, type_ = self.room_name.get(), self.room_type.get()
        if name.isalnum():
            new_room: Room = Room(name, type_)
            ui.events.publish('add_room', new_room)


class LightsMenuWindow(MenuWindow):
    def __init__(self):
        super().__init__('Lights')

    def _build_tabs(self):
        pass
