import tkinter as tk
import asyncio

from .rooms import RoomTabs
from backend.home import Home


class TkRoot(tk.Tk):
    def __init__(self):
        super().__init__()
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.loop = None  # set when run() is called

        # build
        self.room_tabs = RoomTabs(self)
        self.room_tabs.pack()

        # load home
        self.home_model = Home.from_save('0000000')

    def run(self):
        async def tkinter_loop():
            while True:
                self.update()
                await asyncio.sleep(1/30)

        self.loop = asyncio.new_event_loop()

        self.loop.create_task(tkinter_loop())
        self.loop.create_task(self.home_model.update_lights())

        self.loop.run_forever()

    def close(self):
        self.loop.stop()
        self.destroy()
