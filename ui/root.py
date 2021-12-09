
import tkinter as tk
import asyncio

from backend.home import Home
from ui.rooms import RoomTabs
from ui.controls import ControlPanel
from ui.menu import MenuOpener


class TkRoot(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('WizWizard')
        self.protocol("WM_DELETE_WINDOW", self.close)

        # build
        MenuOpener(self).pack(side='top', anchor='ne')
        RoomTabs(self).pack(fill='both', expand=True)
        ControlPanel(self).pack(fill='both', side='bottom')

        # load home
        self.home_model = Home.from_save('0000000')

    async def app_mainloop(self):
        while True:
            self.update()
            await asyncio.sleep(1/60)

    def close(self):
        asyncio.get_running_loop().stop()
        self.destroy()
