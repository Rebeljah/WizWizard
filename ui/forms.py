from kivy.app import App
from kivy.uix.modalview import ModalView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.carousel import Carousel
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton

from functools import partial

from models.room import Room
from models.light import Light
from utils import utils


class AddRoomView(ModalView):
    """Form for adding a selected_room to the home"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()

        self.form = None

    def build(self):
        self.clear_widgets()

        self.form = self.InputForm()
        self.add_widget(self.form)

    def on_open(self):
        self.build()

    def on_dismiss(self):
        """Saves the home after the InputForm has been verified and submitted"""
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
            # build selected_room name input label and text box
            name_label = Label(text="Room name:")
            self.add_widget(name_label)
            self.name_input = TextInput()
            self.add_widget(self.name_input)

            # build selected_room type label and selection carousel
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
            """Verify form data then dismiss AddRoomView to finalize changes"""
            # TODO verify form data before finalizing
            self.parent.dismiss()

        def set_room_type(self, room_type: str, btn):
            if room_type:
                self.room_type = room_type


class AssignLightView(ModalView):
    """Form for adding an unassigned light to a selected_room"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()

    def build(self):
        self.clear_widgets()

        grid = GridLayout(rows=2, padding=20)
        self.add_widget(grid)

        # add selection pane for user to select light to assign
        self.light_grid = self.LightSelectionGrid()
        grid.add_widget(self.light_grid)

        # add form to select selected_room and submit assignment
        self.form = self.RoomAssignForm()
        grid.add_widget(self.form)

    def on_open(self):
        self.build()

    def on_dismiss(self):
        """Assign the light after the RoomAssignForm is submitted"""
        light: Light = self.light_grid.selected_light
        room: Room = self.form.selected_room
        light.name = self.form.light_name
        self.app.home.unassigned_lights.remove(light)
        room.add_light(light)
        self.app.home.save_to_json()
        self.app.re_build()

    class RoomAssignForm(GridLayout):
        """After selecting a light, the user selects a selected_room to assign the
        light to. Holds an area to select a selected_room as well as a submit button"""
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.app = App.get_running_app()

            self.cols = 2
            self.rows = 3

            self.selected_room: Room = None
            self.light_name: str = None

            self.build()

        def build(self):
            # selected_room select carousel
            room_name = Label(text="Room name:")
            self.add_widget(room_name)
            type_carousel = Carousel()
            for room in self.app.home.rooms:
                btn = Button(
                    text=room.name,
                    on_release=partial(self._set_room, room)
                )
                type_carousel.add_widget(btn)
            self.add_widget(type_carousel)

            # light name text input
            self.add_widget(Label(text="Light name:"))
            light_name = TextInput(multiline=False, on_text_validate=self._set_light_name)
            self.add_widget(light_name)

            # add submit button
            submit_btn = Button(
                text="Submit",
                on_release=self._submit
            )
            self.add_widget(submit_btn)

        def _set_room(self, room: Room, btn):
            """Set the selected_room that the light will be assigned to"""
            self.selected_room = room

        def _set_light_name(self, txt_input):
            self.light_name = txt_input.text

        def _submit(self, btn):
            """Dismiss AssignLightView to finalize changes"""
            self.parent.parent.dismiss()

    class LightSelectionGrid(GridLayout):
        """
        Allows the user to select a light to assign to a selected_room
        """
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.app = App.get_running_app()

            self.selected_light: Light = None

            # formatting
            self.rows = 3
            self.cols = 4
            self.padding = 50

            self.build()

        def build(self):
            self.clear_widgets()

            lights = self.app.home.unassigned_lights
            if lights:
                for light in lights:
                    self.add_widget(self.LightSelector(light))
            else:
                no_lights_label = Label(text='No unassigned lights to show!')
                self.add_widget(no_lights_label)

        class LightSelector(ToggleButton):
            """When pressed tells the LightSelectionGrid to hold this buttons
            light as the selected light to assign to a selected_room"""
            def __init__(self, light: Light, **kwargs):
                super().__init__(**kwargs)

                # reference to selected light
                self.light = light

                # button formatting
                self.text = light.name
                self.state = "normal"  # "down"

            def on_press(self):
                """
                Set all other buttons to normal then set self as the
                 LightSelectionGrid's selected light.
                """
                temp_state: str = self.state
                for btn in self.parent.children:
                    btn.state = "normal"
                self.state = temp_state

                if self.state == "down":
                    self.parent.selected_light = self.light
                    self.light.set_brightness(1)
