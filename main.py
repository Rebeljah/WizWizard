import asyncio

from src.backend.home import Home
from src.ui.root import TkRoot


if __name__ == '__main__':

    app = TkRoot()
    home = Home.from_save('0000000')
    loop = asyncio.new_event_loop()

    loop.create_task(app.app_mainloop())
    loop.create_task(home.find_lights())

    loop.run_forever()
