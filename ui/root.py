from kivy.app import App
from kivy.uix.gridlayout import GridLayout

from models.home import Home

from ui.controls import RoomScreenManager
from ui.navbar import NavBar
from ui.forms import AddRoomView, AssignLightView

from utils.utils import create_uid


class WizWizardApp(App):
    """Main app to launch UI"""
    def __init__(self, home: Home, **kwargs):
        super().__init__(**kwargs)
        self.home: Home = home

        # form for adding new rooms
        self.add_room_form = AddRoomView()
        # form for assigning lights to a room
        self.assign_light_form = AssignLightView()

        # overall GridLayout
        self.root = GridLayout(rows=2)

        # add top navbar
        self.nav_bar = NavBar()
        self.root.add_widget(self.nav_bar)

        # add room light control area
        self.room_screen_manager = RoomScreenManager()
        self.root.add_widget(self.room_screen_manager)

    def build(self):
        return self.root

    def re_build(self):
        self.nav_bar.build()
        self.room_screen_manager.build()
        self.add_room_form = AddRoomView()
        self.assign_light_form = AssignLightView()

    def set_current_room(self, room_id):
        self.room_screen_manager.current = room_id
