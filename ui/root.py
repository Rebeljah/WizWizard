
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button

from models.home import Home
from . import navbar


class RootGridLayout(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.clear_widgets()

        self.rows = 3

        # add top navbar
        self.add_widget(widget := navbar.Navbar())
        self.nav_bar = widget

        # TODO DEBUG just for filler
        self.add_widget(Button())


class WizWizardApp(App):
    """Main app to launch UI"""
    def __init__(self, home: Home, **kwargs):
        super().__init__(**kwargs)
        self.home = home

        # main content root
        self.root = RootGridLayout()

    def build(self):
        return self.root

    def on_edit_home(self) -> None:
        """save home data and refresh UI"""
        self.home.save_to_json()
        self.root.__init__()
