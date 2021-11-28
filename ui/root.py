import tkinter as tk
from tkinter import ttk
import asyncio

from .rooms import RoomTabs
from .controls import ControlPanel
from backend.home import Home


class TkRoot(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('WizWizard')
        self.protocol("WM_DELETE_WINDOW", self.close)

        # build
        self.room_tabs = RoomTabs(self)
        self.room_tabs.pack(fill='both', expand=True)
        self.control_panel = ControlPanel(self)
        self.control_panel.pack(fill='both', side='bottom')

        # load home
        self.home_model = Home.from_save('0000000')

    async def app_mainloop(self):
        while True:
            self.update()
            await asyncio.sleep(1/60)

    def close(self):
        asyncio.get_running_loop().stop()
        self.destroy()
