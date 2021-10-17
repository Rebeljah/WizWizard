import asyncio
from ui.root import WizWizardApp


if __name__ == '__main__':
    app = WizWizardApp()
    loop = asyncio.new_event_loop()
    loop.run_until_complete(app.async_run())
    loop.close()
