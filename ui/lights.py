from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.uix.screenmanager import Screen, ScreenManager

from models.light import Light
from utils.utils import get_app_and_root


class LightPageManager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app, self.root = get_app_and_root()
        self.root.add_widget(self)
        self.build()

    def build(self):
        for room in self.app.home.rooms:
            light_page = LightPage(room)
            self.add_widget(light_page)


class LightPage(Screen):
    def __init__(self, room, **kwargs):
        super().__init__(**kwargs)
        self.name = room.id
        self.add_widget(LightGrid(*room.lights))


class LightGrid(GridLayout):
    def __init__(self, *lights, **kwargs):
        super().__init__(**kwargs)
        self.app, self.root = get_app_and_root()

        self.lights: list[Light] = [*lights]

        self.cols = 4
        self.rows = 2
        self.padding = 50

        self.build()

    def build(self):
        self.clear_widgets()
        for light in self.lights:
            if light.available:
                self.add_widget(self.LightControlPanel(light))
            else:
                self.add_widget(Label(text=f"{light.name} disconnected"))

    def set_lights(self, lights) -> None:
        self.lights = list(lights)
        self.build()

    class LightControlPanel(GridLayout):
        def __init__(self, light, **kwargs):
            super().__init__(**kwargs)

            self.rows = 3
            self.light = light
            self.text = light.name

            self.build()

        def build(self):
            self.add_widget(Label(text=self.light.name))

            on_off_button = Button(
                    text='on/off',
                    on_release=self.toggle_light
            )
            self.add_widget(on_off_button)

            brightness_slider = Slider(
                min=0,
                max=255,
                value=self.light.brightness
            )
            brightness_slider.bind(value=self.set_brightness)
            self.add_widget(brightness_slider)

        def toggle_light(self, btn):
            self.light.toggle()

        def set_brightness(self, slider, brightness):
            self.light.set_brightness(brightness)
