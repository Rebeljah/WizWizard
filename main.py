import tkinter as tk
from tkinter import ttk
import asyncio


class AppRoot(tk.Tk):
    def __init__(self, loop):
        super().__init__()
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.loop = loop

        self.build()
        self.loop.create_task(self.run())

    def build(self):
        pass

    async def run(self):
        while True:
            self.update()
            await asyncio.sleep(1/30)

    def close(self):
        self.loop.stop()
        self.destroy()


if __name__ == '__main__':
    def main():
        loop = asyncio.get_event_loop()
        root = AppRoot(loop)
        loop.run_forever()

    main()
