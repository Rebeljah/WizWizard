from kivy.app import App
from kivy.uix.modalview import ModalView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.carousel import Carousel
from kivy.uix.button import Button

from functools import partial

from models.room import Room
from utils import utils


class AddRoomView(ModalView):
    """Form for adding a room to the home"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()

        self.form = None
        self.build()

    def build(self):
        self.clear_widgets()

        self.form = self.InputForm()
        self.add_widget(self.form)

    def on_open(self):
        pass

    def on_dismiss(self):
        self.app.home.add_room(
            Room(
                self.form.name_input.text,
                self.form.room_type,
                utils.create_uid()
            )
        )
        self.app.home.save_to_json()
        self.app.re_build()

    class InputForm(GridLayout):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)

            self.room_type: str = ''
            self.name_input = None

            # formatting
            self.rows = 3
            self.cols = 2

            self.build()

        def build(self):
            # build room name input label and text box
            name_label = Label(text="Room name:")
            self.add_widget(name_label)
            self.name_input = TextInput()
            self.add_widget(self.name_input)

            # build room type label and selection carousel
            type_label = Label(text="Room type:")
            self.add_widget(type_label)
            type_carousel = Carousel()
            for room_type in Room.room_types:
                btn = Button(
                    text=room_type,
                    on_release=partial(self.set_room_type, room_type)
                )
                type_carousel.add_widget(btn)
            self.add_widget(type_carousel)

            # add submit button
            submit_btn = Button(
                text="Submit",
                on_release=self._submit
            )
            self.add_widget(submit_btn)

        def _submit(self, btn):
            self.parent.dismiss()

        def set_room_type(self, room_type: str, btn):
            if room_type:
                self.room_type = room_type


class AssignLightView(ModalView):
    """Form for adding an unassigned light to a room"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()

        self.form = None
        self.build()

    def build(self):
        self.clear_widgets()

        self.form = self.InputForm()
        self.add_widget(self.form)

    def on_open(self):
        pass

    def on_dismiss(self):
        # TODO add a new light to the home here
        self.app.home.save_to_json()
        self.app.re_build()

    class InputForm(GridLayout):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)

            self.build()

        def build(self):
            # TODO finish this
            pass

        def _submit(self, btn):
            """Dismiss the AssignLightView that holds this form"""
            self.parent.dismiss()
