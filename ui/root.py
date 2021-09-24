from kivy.uix.gridlayout import GridLayout

from models.home import Home
from ui.lights import LightGrid
from ui.rooms import RoomGrid
from ui.navbar import NavbarGrid


class RootGrid(GridLayout):
    def __init__(self, home: Home, **kwargs):
        super().__init__(**kwargs)
        self.home_model = home

        self.rows = 3
        self.room_grid = RoomGrid(self)
        self.light_grid = LightGrid(self)
        self.navbar_grid = NavbarGrid(self)

    def set_visible_lights(self, lights):
        self.light_grid.set_lights(lights)
