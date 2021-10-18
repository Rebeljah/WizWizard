import asyncio
from ui.root import WizWizardApp
from backend.home import Home


if __name__ == '__main__':
    loop = asyncio.new_event_loop()

    home = loop.run_until_complete(Home.from_save('0000000'))
    app = WizWizardApp(home)
    loop.run_until_complete(app.async_run())

    loop.close()
