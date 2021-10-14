
from kivy.app import App
from kivy.uix.gridlayout import GridLayout

from backend.home import Home
from backend.room import Room
from ui.navbar import Navbar
from ui.light_area import LightArea
from ui.control_panel import ControlPanel


class RootGridLayout(GridLayout):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.rows = 3

        self.navbar = Navbar
        self.light_area = LightArea
        self.control_panel = ControlPanel
        self.build()

    def build(self):
        self.clear_widgets()

        # add top navbar
        self.navbar = Navbar()
        self.add_widget(self.navbar)

        # add light selection area
        self.light_area = LightArea()
        self.add_widget(self.light_area)

        # add control panel
        self.control_panel = ControlPanel()
        self.add_widget(self.control_panel)

    def set_shown_room(self, room: Room):
        self.light_area.set_room(room)


class WizWizardApp(App):
    """Main app to launch UI"""
    def __init__(self, home: Home, **kwargs):
        super().__init__(**kwargs)
        self.home = home

        # main content root
        self.root = RootGridLayout(self)

    def build(self):
        return self.root

    def on_edit_home(self) -> None:
        """save home data and refresh UI"""
        self.home.save_to_json()
        self.root.build()
