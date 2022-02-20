import asyncio
from tkinter.simpledialog import askstring

from src.backend import home
from src.ui import root


if __name__ == '__main__':
    loop = asyncio.new_event_loop()

    app = root.TkRoot()
    loop.create_task(app.app_mainloop())

    if (loaded_home := home.Home.get_last_loaded()) is None:
        loaded_home = home.Home(askstring('New home', 'Home name'))
        loaded_home.save_to_json()

    loop.create_task(loaded_home.find_lights())

    loop.run_forever()
