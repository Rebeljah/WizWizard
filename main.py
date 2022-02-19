import asyncio
from tkinter.simpledialog import askstring

from src.backend import home
from src.ui import root, menu


if __name__ == '__main__':
    # create app first so it can react to backend setup
    loop = asyncio.new_event_loop()

    app = root.TkRoot()
    loop.create_task(app.app_mainloop())

    home = home.Home.get_last_loaded_home() or home.Home(askstring('New home', 'Home name'))

    loop.create_task(home.find_lights())

    loop.run_forever()
