from pathlib import Path
import tkinter as tk
import asyncio

from src.ui import menu, rooms, controls
from . import utils


class TkRoot(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('WizWizard')
        self.iconphoto(True, utils.get_image('icon'))
        self.protocol("WM_DELETE_WINDOW", self.close)

        # Build app content
        menu.MenuOpener(self).pack(side='top', anchor='ne')
        rooms.RoomTabs(self).pack(fill='both', expand=True)
        controls.ControlPanel(self).pack(fill='both', side='bottom')

    async def app_mainloop(self):
        while True:
            self.update()
            await asyncio.sleep(1/10)

    def close(self):
        asyncio.get_running_loop().stop()
        self.destroy()
