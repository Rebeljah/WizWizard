"""Module to contain code related to menus"""

import tkinter as tk
from tkinter import ttk

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
    def __init__(self, title):
        super().__init__()
        self.title(title)
        self.menu = ttk.Notebook(self)
        self.menu.pack()


class RoomsMenuWindow(MenuWindow):
    def __init__(self):
        super().__init__('Rooms')

        # self.menu.add(ttk.Button(self), text='test')
        """Add a notebook tab for each room in the home (re-use code from rooms.py?)
        Inside of each tab will be user dialog frame that can be different
        depending on the tab (tk.Frame).
        
        At the end of the tabs will be the 'add room' tab"""
