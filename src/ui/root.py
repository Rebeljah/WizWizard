
import tkinter as tk
import asyncio

from src.ui import menu, rooms, controls


class TkRoot(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('WizWizard')
        self.protocol("WM_DELETE_WINDOW", self.close)

        # build
        menu.MenuOpener(self).pack(side='top', anchor='ne')
        rooms.RoomTabs(self).pack(fill='both', expand=True)
        controls.ControlPanel(self).pack(fill='both', side='bottom')

    async def app_mainloop(self):
        while True:
            self.update()
            await asyncio.sleep(1/60)

    def close(self):
        asyncio.get_running_loop().stop()
        self.destroy()
