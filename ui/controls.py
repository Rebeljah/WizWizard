from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.slider import Slider
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.app import App

from models.light import Light
from models.room import Room


class RoomScreenManager(ScreenManager):
    """
    Holds a RoomControlPage for each room in the Home . Each page allows the
    user to select and control lights in a room.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()

        self.build()

    def build(self):
        self.clear_widgets()
        room: Room
        for room in self.app.home.rooms:
            page = RoomControlPage(room)
            self.add_widget(page)


class RoomControlPage(Screen):
    """
    A screen to allow the user to select and control lights in a room. Belongs
    to the RoomScreenManager object and has a LightSelectionGrid and a ControlPanel.
    """
    def __init__(self, room: Room, **kwargs):
        super().__init__(**kwargs)
        self.name = room.id  # used for switching screens

        # the room this page controls
        self.room: Room = room

        # formatting
        self.rows = 2

        # create inner grid and add selection area and control panel
        self.grid = GridLayout(rows=2)
        self.add_widget(self.grid)
        # add light selector and control panel to self.grid
        self.light_selector = self.LightSelectionGrid(self.room.lights)
        self.control_panel = self.ControlPanel(self.room.lights)
        self.grid.add_widget(self.light_selector)
        self.grid.add_widget(self.control_panel)

    class LightSelectionGrid(GridLayout):
        """
        Allows the user to select multiple lights to edit at once. Belongs to a
        RoomControlPage.
        """
        def __init__(self, lights: list[Light], **kwargs):
            super().__init__(**kwargs)

            # list to hold lights that are displayed
            self.visible_lights: list[Light] = lights[:]

            # formatting
            self.rows = 3
            self.cols = 4
            self.padding = 50

            self.build()

        def build(self):
            # build
            for light in self.visible_lights:
                self.add_widget(self.LightSelector(light))

        class LightSelector(ToggleButton):
            def __init__(self, light: Light, **kwargs):
                super().__init__(**kwargs)

                # reference to controlled light
                self.light = light

                # button formatting
                self.text = light.name

                # button press / release behavior
                self.state = "down"  # "normal"
                self.bind(state=self.on_toggle)

            def on_toggle(self, btn, state):
                control_page = self.parent.parent.parent
                if self.state == "down":
                    control_page.control_panel.add_light(self.light)
                else:
                    control_page.control_panel.remove_light(self.light)

    class ControlPanel(GridLayout):
        """
        A control panel to edit the state of the lights in a room selected by the
        LightSelectionGrid. Belongs to a RoomControlPage.
        """
        def __init__(self, lights: list[Light], **kwargs):
            super().__init__(**kwargs)

            # formatting
            self.rows = 3
            self.size_hint_y = 0.33
            self.padding = 10

            # list to hold the lights that this panel controls.
            self.controlled_lights = set(lights)

            self.build()

        def build(self):
            # brightness slider; get starting brightness
            brightnesses = tuple(l.brightness for l in self.controlled_lights if l.is_on)
            if len(brightnesses):
                brightness = max(brightnesses)
            else:
                brightness = 0
            slider = Slider(
                min=0,
                max=255,
                value=brightness
            )
            slider.bind(value=self._set_brightness)  # bind value change
            self.add_widget(slider)

            # on/off button
            btn = Button(
                text='on/off',
                on_release=self._toggle_lights
            )
            self.add_widget(btn)

        def _toggle_lights(self, btn):
            light: Light
            for light in self.controlled_lights:
                light.toggle()

        def _set_brightness(self, slider, brightness_value):
            light: Light
            for light in self.controlled_lights:
                light.set_brightness(brightness_value)

        def add_light(self, light: Light):
            self.controlled_lights.add(light)

        def remove_light(self, light):
            self.controlled_lights.remove(light)
