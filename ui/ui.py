from kivy.app import App

from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button


class MainGrid(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rows = 3

        self.room_grid = RoomGrid()
        self.add_widget(self.room_grid)

        self.light_grid = LightGrid()
        self.add_widget(self.light_grid)

        self.navbar_grid = NavbarGrid()
        self.add_widget(self.navbar_grid)


class RoomGrid(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 7
        self.rows = 1
        self.size_hint_y = 0.2


class LightGrid(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 4
        self.rows = 2
        self.padding = 50


class NavbarGrid(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 4
        self.rows = 1
        self.padding = 20
        self.size_hint_y = 0.25


class WizWizardApp(App):
    """Main app to launch UI"""
    def build(self):
        return MainGrid()
