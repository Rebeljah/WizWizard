from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button

from utils.utils import get_app_and_root


class NavbarGrid(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app, self.root = get_app_and_root()
        self.root.add_widget(self)

        self.cols = 4
        self.rows = 1
        self.padding = 20
        self.size_hint_y = 0.25

        self.build()

    def build(self):
        btn = Button(text='toggle all')
        self.add_widget(btn)
        btn = Button(text='theme all')
        self.add_widget(btn)
        btn = Button(text='schedule')
        self.add_widget(btn)
        btn = Button(text='menu')
        self.add_widget(btn)
