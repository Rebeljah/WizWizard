from kivy.app import App
from kivy.uix.dropdown import DropDown

from typing import Any


class ItemDropDown(DropDown):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()

        self._selected_value: Any = None

    @property
    def selected_value(self):
        return self._selected_value

    def select_(self, value, btn):
        """Alias to DropDown.select() which takes an unused button arg from the
        dropdown when selected"""
        self.select(value)

    def on_select(self, value: Any):
        self._selected_value = value
