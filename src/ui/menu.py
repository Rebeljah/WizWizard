"""Module to contain code related to menus"""

import tkinter as tk
from tkinter import ttk

from typing import Callable
from abc import ABC, abstractmethod

from src import ui
from src.utils.observer import Event
from src.ui.utils import get_image
from src.backend.room import Room
from src.backend.home import Home


class Widgets:
    """Defines factory methods for generic widgets"""
    @staticmethod
    def room_name_input(parent, room_name_var) -> ttk.Labelframe:
        frame = ttk.Labelframe(parent, text='edit room name')
        room_name_entry = ttk.Entry(frame, textvariable=room_name_var)
        room_name_entry.pack()
        return frame

    @staticmethod
    def dropdown_input(parent, title, options, var) -> ttk.Labelframe:
        frame = ttk.Labelframe(parent, text=title)
        dropdown = ttk.OptionMenu(
            frame, var, '--', *options
        )
        dropdown.pack()
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
        self.home: Home = Home.active_home
        self.tabs = ttk.Notebook(self)

    @abstractmethod
    def _build_tabs(self):
        pass


class MenuTab(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)


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
        self.tabs.add(self.EditRoomsTab(self), text='Edit Rooms')
        self.tabs.add(self.CreateRoomTab(self), text='+Add Room')

    class CreateRoomTab(MenuTab):
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
            name_input.pack(side='top')

            type_input = Widgets.dropdown_input(self, 'edit room type', Room.room_types, self.room_type)
            type_input.pack(side='top')

        def _submit(self):
            room_name = self.room_name.get()
            room_type = self.room_type.get()

            if not room_name.replace(' ', '').isalnum():
                return

            ui.events.publish(Event.AddedRoom, Room(room_name, room_type))

            # close the menu
            self.nametowidget(self.winfo_parent()).destroy()

    class EditRoomsTab(MenuTab):
        """Frame that contains settings dialogs for rooms in the home."""
        def __init__(self, parent):
            super().__init__(parent)

            # define user changeable variables
            self.selected_room_name = tk.StringVar()
            self.room_name = tk.StringVar()
            self.room_type = tk.StringVar()

            self.content_frame = ttk.Frame(self)
            self._build_content()
            self.content_frame.pack()

            submit_button = Widgets.submit_button(self, self._submit)
            submit_button.pack(side='bottom', anchor='se')

        def _build_content(self):
            # build a dropdown that lists the rooms available.
            room_selector = Widgets.dropdown_input(
                self, 'Room', Room.saved_rooms(), self.selected_room_name
            )
            room_selector.pack(side='top')

            name_input = Widgets.room_name_input(
                self.content_frame, self.room_name
            )
            name_input.pack(side='top')

            type_input = Widgets.dropdown_input(self, 'room type', Room.room_types, self.room_type)
            type_input.pack(side='top')

        def _submit(self):
            selected_room_name = self.selected_room_name.get()
            room_type = self.room_type.get()
            room_name = self.room_name.get()
            edited = False

            room = Room.from_name(selected_room_name)
            if room is None:
                return  # user did not select a room

            # edit the room with input verification
            if room_type in Room.room_types:
                room.type = room_type
                edited = True
            if room_name.replace(' ', '').isalnum():
                room.name = room_name
                edited = True

            if not edited:
                return  # user made no changes

            ui.events.publish(Event.EditedRoom, room)
            print(room, room.name, room.type)
            # close the menu
            self.nametowidget(self.winfo_parent()).destroy()


class LightsMenuWindow(MenuWindow):
    def __init__(self):
        super().__init__('Lights')

    def _build_tabs(self):
        pass
