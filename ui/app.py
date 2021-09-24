from kivy.app import App

from models.home import Home
from ui.root import RootGrid


class WizWizardApp(App):
    """Main app to launch UI"""
    def __init__(self, home: Home, **kwargs):
        super().__init__(**kwargs)
        self.home: Home = home

    def build(self):
        return RootGrid(self.home)
