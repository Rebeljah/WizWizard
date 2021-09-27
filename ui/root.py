from kivy.app import App
from kivy.uix.gridlayout import GridLayout

from models.home import Home
from ui.room_controls import RoomControlPageManager
from ui.room_navbar import RoomNavbar


class RootGrid(GridLayout):
    def __init__(self, app: App, **kwargs):
        super().__init__(**kwargs)
        app.root = self

        # formatting
        self.rows = 3

        # add children
        self.room_navbar = RoomNavbar()
        self.room_controls = RoomControlPageManager()
        self.add_widget(self.room_navbar)
        self.add_widget(self.room_controls)


class WizWizardApp(App):
    """Main app to launch UI"""
    def __init__(self, home: Home, **kwargs):
        super().__init__(**kwargs)
        self.home: Home = home

    def build(self):
        return RootGrid(self)
