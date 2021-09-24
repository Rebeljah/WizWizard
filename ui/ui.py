from kivy.app import App

from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button

from functools import partial

from models.home import Home
from models.light import Light

# typing
Lights = list[Light]


class RoomGrid(GridLayout):
    def __init__(self, root, **kwargs):
        super().__init__(**kwargs)
        assert root.parent is None
        root.add_widget(self)

        self.cols = 7
        self.rows = 1
        self.size_hint_y = 0.2

        self.build()

    def build(self) -> None:
        root: RootGrid = self.parent
        for room in root.home_model.rooms:
            btn = Button(
                text=room.name,
                on_release=partial(root.set_lights, room.lights)
            )
            self.add_widget(btn)


class LightGrid(GridLayout):
    def __init__(self, root, **kwargs):
        super().__init__(**kwargs)
        root.add_widget(self)

        self.lights: Lights = []

        self.cols = 4
        self.rows = 2
        self.padding = 50

        self.build()

    def build(self):
        root: RootGrid = self.parent
        self.clear_widgets()
        if self.lights:
            for light in self.lights:
                btn = Button(text=light.name)
                self.add_widget(btn)
        else:
            self.add_widget(Button(text='no lights'))

    def set_lights(self, lights) -> None:
        self.lights = list(lights)
        self.build()


class NavbarGrid(GridLayout):
    def __init__(self, root, **kwargs):
        super().__init__(**kwargs)
        root.add_widget(self)

        self.cols = 4
        self.rows = 1
        self.padding = 20
        self.size_hint_y = 0.25

        self.build()

    def build(self):
        root: RootGrid = self.parent

        btn = Button(text='toggle all')
        self.add_widget(btn)
        btn = Button(text='theme all')
        self.add_widget(btn)
        btn = Button(text='schedule')
        self.add_widget(btn)
        btn = Button(text='menu')
        self.add_widget(btn)


class RootGrid(GridLayout):
    def __init__(self, home: Home, **kwargs):
        super().__init__(**kwargs)
        self.home_model = home

        self.rows = 3
        self.room_grid = RoomGrid(self)
        self.light_grid = LightGrid(self)
        self.navbar_grid = NavbarGrid(self)

    def set_lights(self, lights, _) -> None:
        self.light_grid.set_lights(lights)


class WizWizardApp(App):
    """Main app to launch UI"""
    def __init__(self, home: Home, **kwargs):
        super().__init__(**kwargs)
        self.home: Home = home

    def build(self):
        return RootGrid(self.home)
