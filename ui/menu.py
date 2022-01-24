"""Module to contain code related to menus"""

import tkinter as tk
from tkinter import ttk

from typing import Optional, Callable
from abc import ABC, abstractmethod

import backend
import ui
from backend.home import Home
from backend.room import Room
from ui.utils import get_image


class Widgets:
    """Defines factory methods for generic widgets"""
    @staticmethod
    def room_name_input(parent, room_name_var) -> ttk.Labelframe:
        frame = ttk.Labelframe(parent, text='Room name:')
        room_name_entry = ttk.Entry(frame, textvariable=room_name_var)
        room_name_entry.pack()
        return frame

    @staticmethod
    def room_type_input(parent, room_type_var) -> ttk.Labelframe:
        frame = ttk.Labelframe(parent, text='Room type:')
        room_type_selector = ttk.OptionMenu(
            frame, room_type_var, Room.room_types[0], *Room.room_types
        )
        room_type_selector.pack()
        return frame

    @staticmethod
    def submit_button(parent, command: Callable) -> ttk.Button:
        submit_button = ttk.Button(
            parent, text='Submit', command=command
        )
        return submit_button


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


class MenuOpener(ttk.Menubutton):
    def __init__(self, parent):
        super().__init__(parent)
        self.config(image=get_image('menu_burger_b'))
        self.config(menu=self._build_menu())

    def _build_menu(self) -> tk.Menu:
        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label='Rooms', command=RoomsMenuWindow)
        menu.add_command(label='Lights', command=LightsMenuWindow)
        return menu


class RoomsMenuWindow(MenuWindow):
    """Toplevel window that contains settings dialogs to edit or add rooms"""
    def __init__(self):
        super().__init__('Rooms')
        self._build_tabs()
        self.tabs.pack()

    def _build_tabs(self):
        self.tabs.add(self.RoomSettingsTab(self), text='Edit Rooms')
        self.tabs.add(self.CreateRoomTab(self), text='+Add Room')

    class CreateRoomTab(ttk.Frame):
        """Dialog to enter a name and select a type for a new room"""
        def __init__(self, parent):
            super().__init__(parent)

            # define user changeable variables
            self.room_name = tk.StringVar()
            self.room_type = tk.StringVar()

            self.content_frame = ttk.Frame(self)
            self._build_content()
            self.content_frame.pack(side='top', padx=50)

            submit_button = Widgets.submit_button(self, self._submit)
            submit_button.pack(side='bottom', anchor='se')

        def _build_content(self):
            name_input = Widgets.room_name_input(
                self.content_frame, self.room_name
            )
            name_input.pack(side='top', anchor='w')

            type_input = Widgets.room_type_input(
                self.content_frame, self.room_type
            )
            type_input.pack(side='top', anchor='w')

        def _submit(self):
            name, type_ = self.room_name.get(), self.room_type.get()
            if name.isalnum():
                ui.events.publish('add_room', Room(name, type_))

    class RoomSettingsTab(ttk.Frame):
        """Frame that contains settings dialogs for rooms in the home."""
        def __init__(self, parent):
            super().__init__(parent)

            # define user changeable variables
            self.selected_room: Optional[Room] = None
            self.room_name = tk.StringVar()
            self.room_type = tk.StringVar()

            self.content_frame = ttk.Frame(self)
            self._build_content()
            self.content_frame.pack()

            submit_button = Widgets.submit_button(self, self._submit)
            submit_button.pack(side='bottom', anchor='se')

        def _build_content(self):
            name_input = Widgets.room_name_input(
                self.content_frame, self.room_name
            )
            name_input.pack(side='top', anchor='w')

            type_input = Widgets.room_type_input(
                self.content_frame, self.room_type
            )
            type_input.pack(side='top', anchor='w')

        def _submit(self):
            pass


class LightsMenuWindow(MenuWindow):
    def __init__(self):
        super().__init__('Lights')

    def _build_tabs(self):
        pass
