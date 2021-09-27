from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.slider import Slider
from kivy.uix.screenmanager import Screen, ScreenManager

from models.light import Light
from models.room import Room
from utils.utils import get_app_and_root


class RoomControlPageManager(ScreenManager):
    """
    Holds a RoomControlPage for each room in the Home . Each page allows the
    user to select lights an a room and change their states.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app, self.root = get_app_and_root()

        self.build()

    def build(self):
        room: Room
        for room in self.app.home.rooms:
            page = RoomControlPage(room)
            self.add_widget(page)


class RoomControlPage(Screen):
    controlled_lights = []
    """
    A screen to allow the user to select lights in a room and control the state
    of those lights. Belongs to the RoomControlPageManager object and has a
    LightSelectArea and a SelectedLightsControlPanel.
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
        self.light_selector = self.LightSelectArea(self.room.lights)
        self.lights_controller = self.ControlPanel(self.room.lights)
        self.grid.add_widget(self.light_selector)
        self.grid.add_widget(self.lights_controller)

    class LightSelectArea(GridLayout):
        """
        Allows the user to select multiple lights to edit at once. Belongs to a
        RoomControlPage. Automatically added to RoomControlPage on init.
        """
        def __init__(self, lights: list[Light], **kwargs):
            super().__init__(**kwargs)

            # list to hold lights that are displayed
            self.visible_lights: list[Light] = lights[:]

            # formatting
            self.rows = 3
            self.cols = 4
            self.padding = 10

            # build
            for light in self.visible_lights:
                self.add_widget(
                    self.LightSelectorToggle(light)
                )

        class LightSelectorToggle(ToggleButton):
            def __init__(self, light: Light, **kwargs):
                super().__init__(**kwargs)
                _, root = get_app_and_root()
                # formatting
                self.text = light.name

                # reference to controlled light
                self.light = light

                # button press / release behavior
                self.state = "down"  # "normal"
                self.bind(state=self.state_change)

            def state_change(self, btn, state):
                control_page = self.parent.parent.parent
                if self.state == "down":
                    control_page.lights_controller.control(self.light)
                else:
                    control_page.lights_controller.release(self.light)

    class ControlPanel(GridLayout):
        """
        A control panel to edit the state of the lights in a room selected by the
        LightSelectArea. Belongs to a RoomControlPage.
        """
        def __init__(self, lights: list[Light], **kwargs):
            super().__init__(**kwargs)

            # formatting
            self.rows = 3
            self.size_hint_y = 0.33
            self.padding = 10

            # list to hold the lights that this panel controls.
            self.controlled_lights = set(lights)

            # build
            btn = Button(
                text='on/off',
                on_release=self._toggle_lights
            )
            self.add_widget(btn)
            brightness = max(l.brightness for l in lights)
            slider = Slider(
                min=0,
                max=255,
                value=brightness
            )
            slider.bind(value=self._set_brightness)
            self.add_widget(slider)

        def _toggle_lights(self, btn):
            light: Light
            for light in self.controlled_lights:
                light.toggle()

        def _set_brightness(self, slider, brightness_value):
            light: Light
            for light in self.controlled_lights:
                light.set_brightness(brightness_value)

        def control(self, light: Light):
            self.controlled_lights.add(light)

        def release(self, light):
            self.controlled_lights.remove(light)
