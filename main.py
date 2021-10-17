import asyncio

from ui.root import WizWizardApp
from backend.home import Home


def main():
    # TODO handle literal home id here
    home = Home.from_save("0000000")
    app = WizWizardApp(home)

    loop = asyncio.new_event_loop()
    loop.run_until_complete(app.async_run(async_lib='asyncio'))
    loop.close()


if __name__ == '__main__':
    main()
