from kivy.app import App

from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button

# TODO DEBUG
from models.home import Home
home = Home.from_save('3827676')


class MainGrid(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.rows = 3
        self.room_grid = RoomGrid(self)
        self.light_grid = LightGrid(self)
        self.navbar_grid = NavbarGrid(self)


class RoomGrid(GridLayout):
    def __init__(self, parent, **kwargs):
        super().__init__(**kwargs)
        parent.add_widget(self)

        self.cols = 7
        self.rows = 1
        self.size_hint_y = 0.2

        # TODO DEBUG
        global home
        for room in home.rooms:
            button = Button(text=room.name)
            self.add_widget(button)


class LightGrid(GridLayout):
    def __init__(self, parent, **kwargs):
        super().__init__(**kwargs)
        parent.add_widget(self)

        self.cols = 4
        self.rows = 2
        self.padding = 50


class NavbarGrid(GridLayout):
    def __init__(self, parent, **kwargs):
        super().__init__(**kwargs)
        parent.add_widget(self)

        self.cols = 4
        self.rows = 1
        self.padding = 20
        self.size_hint_y = 0.25


class WizWizardApp(App):
    """Main app to launch UI"""
    def build(self):
        return MainGrid()
