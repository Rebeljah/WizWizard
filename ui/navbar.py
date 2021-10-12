from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown

from . import forms


class Navbar(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # formatting
        self.cols = 9
        self.size_hint_y = 0.2
        self.padding = 10

        self.build()

    def build(self):
        def build_room_buttons():
            """Build the buttons for selecting the room to be controlled"""
            pass

        def build_dropdown():
            """Build dropdown to hold add item buttons"""
            # button to open dropdown
            dropdown = dropdown = DropDown()
            self.add_widget(Button(
                text='Menu',
                on_release=dropdown.open
            ))
            dropdown.add_widget(Button(
                size_hint_y=None,
                height=44,
                text='+ Room',
                on_release=lambda btn: forms.AddRoomForm().open()
            ))
            dropdown.add_widget(Button(
                size_hint_y=None,
                height=44,
                text='+ Light',
                on_release=lambda btn: forms.AddLightForm().open()
            ))

        self.clear_widgets()

        build_room_buttons()
        build_dropdown()
