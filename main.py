from ui.root import WizWizardApp
from backend.home import Home


if __name__ == '__main__':
    # TODO handle literal home id here
    home = Home.from_save("0000000")
    app = WizWizardApp(home)
    app.run()
