from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.slider import Slider

from models.light import Light


class LightGrid(GridLayout):
    def __init__(self, root, **kwargs):
        assert root.parent is None
        super().__init__(**kwargs)
        root.add_widget(self)

        self.lights: list[Light] = []

        self.cols = 4
        self.rows = 2
        self.padding = 50

        self.build()

    def build(self):
        root = self.parent
        self.clear_widgets()
        if self.lights:
            for light in self.lights:
                self.add_widget(LightControlPanel(light))

    def set_lights(self, lights) -> None:
        self.lights = list(lights)
        self.build()


class LightControlPanel(GridLayout):
    def __init__(self, light, **kwargs):
        super().__init__(**kwargs)
        self.light = light

        self.rows = 2
        self.text = light.name
        self.on_release = self.toggle_light

        self.build()

    def build(self):
        self.add_widget(
            Button(text='ON/OFF', on_release=self.toggle_light)
        )
        self.add_widget(self.BrightnessSlider())

    def toggle_light(self, btn):
        self.light.toggle()

    class BrightnessSlider(Slider):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)

            self.min = 0
            self.max = 255
            self.value = 100

            self.on_touch_up = self.set_brightness

        def set_brightness(self, _):
            self.parent.light.set_brightness(self.value)
