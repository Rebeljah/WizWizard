import asyncio

from src.backend import home
from src.ui import root


if __name__ == '__main__':
    # create app first so it can react to backend setup
    loop = asyncio.new_event_loop()

    app = root.TkRoot()
    loop.create_task(app.app_mainloop())

    home = home.Home.from_save('0000000')
    loop.create_task(home.find_lights())

    loop.run_forever()
