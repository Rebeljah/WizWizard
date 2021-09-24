from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button



class NavbarGrid(GridLayout):
    def __init__(self, root, **kwargs):
        assert root.parent is None
        super().__init__(**kwargs)
        root.add_widget(self)

        self.cols = 4
        self.rows = 1
        self.padding = 20
        self.size_hint_y = 0.25

        self.build()

    def build(self):
        root = self.parent

        btn = Button(text='toggle all')
        self.add_widget(btn)
        btn = Button(text='theme all')
        self.add_widget(btn)
        btn = Button(text='schedule')
        self.add_widget(btn)
        btn = Button(text='menu')
        self.add_widget(btn)
