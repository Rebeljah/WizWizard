from kivy.app import App
from kivy.uix.gridlayout import GridLayout

from models.home import Home
from ui.lights import LightPageManager
from ui.rooms import RoomGrid
from ui.navbar import NavbarGrid


class RootGrid(GridLayout):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        app.root = self

        self.rows = 3
        self.room_grid = RoomGrid()
        self.light_pages = LightPageManager()
        self.navbar_grid = NavbarGrid()


class WizWizardApp(App):
    """Main app to launch UI"""
    def __init__(self, home: Home, **kwargs):
        super().__init__(**kwargs)
        self.home: Home = home

    def build(self):
        return RootGrid(self)
