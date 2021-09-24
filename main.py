from ui.app import WizWizardApp
from models.home import Home


if __name__ == '__main__':
    # home = Home.from_save("3827676")
    home = Home.from_save("3827676")
    app = WizWizardApp(home)
    app.run()
