import asyncio

from ui.root import TkRoot


if __name__ == '__main__':
    app = TkRoot()
    loop = asyncio.new_event_loop()

    loop.create_task(app.app_mainloop())
    loop.create_task(app.home_model.find_lights())

    loop.run_forever()
