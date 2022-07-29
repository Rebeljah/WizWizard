import asyncio

from src.backend import home
from src.ui import root


def main():
    current_home = home.Home.get_last_loaded()

    if not current_home:
        return

    loop = asyncio.new_event_loop()
    app = root.TkRoot()
    loop.create_task(app.app_mainloop())

    loop.create_task(current_home.find_lights())

    loop.run_forever()


if __name__ == '__main__':
    main()
