"""
Class to hold different forms. Forms inherit from the kivy ModalView class and
    appear on top of the app's root widget.
"""

from kivy.app import App
from kivy.uix.modalview import ModalView
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown

from functools import partial
from abc import abstractmethod
from typing import Any

from backend.room import Room
from ui import popup


class FormABC(ModalView):
    """Base class for all forms"""
    @abstractmethod
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()
        self.padding = 10

    @abstractmethod
    def build(self):
        """Build form widgets"""
        pass

    def submit(self, btn):
        """Verify form, then close the form view"""
        if self._form_is_valid():
            self._do_form_actions()
            self.dismiss()
        else:
            # reset form and display error popup
            self.__init__()
            popup.show_notification('Form is invalid')

    @abstractmethod
    def _form_is_valid(self) -> bool:
        """Called by submit() in order to verify form data"""
        pass

    @abstractmethod
    def _do_form_actions(self):
        """Use the verified form data to do something"""
        pass


class AddRoomForm(FormABC):
    """
    Form for adding a room to the home

    This form contains a submit button and text boxes for the room name and
    type.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout = GridLayout(rows=3, cols=2)
        self.add_widget(self.layout)

        # form fields
        self.room_name = TextInput(multiline=False)
        self.room_type = TextInput(multiline=False)

        self.build()

    def build(self):
        # room name input
        self.layout.add_widget(Label(
            text='Room name',
        ))
        self.layout.add_widget(self.room_name)

        # room type input
        self.layout.add_widget(Label(
            text='Room type'
        ))
        self.layout.add_widget(self.room_type)

        # submit / cancel buttons
        self.layout.add_widget(Button(
            text='Submit',
            on_release=self.submit
        ))
        self.layout.add_widget(Button(
            text='Cancel',
            on_release=self.dismiss
        ))

    def _form_is_valid(self) -> bool:
        return all((
            self.room_name.text,
            self.room_type.text,
            self.room_type.text.lower() in Room.room_types
        ))

    def _do_form_actions(self):
        """create a new room from the form data and add it to the current home"""
        app = App.get_running_app()
        new_room = Room(self.room_name.text, self.room_type.text)
        app.home.add_room(new_room)
        app.on_edit_home()


class AddLightForm(FormABC):
    """Form for adding an unassigned light to a room"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()

        self.layout = GridLayout(rows=5)
        self.layout.size_hint = (.9, .9)
        self.add_widget(self.layout)

        # form fields
        self.light_dropdown = ItemDropDown()
        self.room_dropdown = ItemDropDown()
        self.light_name = TextInput()

        self.build()

    def build(self):
        # button to open dropdown menu
        self.layout.add_widget(Button(
            text='Select a light',
            on_release=self.light_dropdown.open
        ))
        # add items to light dropdown menu
        for light in self.app.home.unassigned.lights:
            self.light_dropdown.add_widget(Button(
                text=light.mac,
                size_hint_y=None,
                height=int(1 / 10 * self.app.root.height),
                on_release=partial(self.light_dropdown.select_, light)
            ))

        # button to open room dropdown
        self.layout.add_widget(Button(
            text='Select a room',
            on_release=self.room_dropdown.open
        ))
        # add items to room dropdown menu
        rooms = self.app.home.rooms
        for room in rooms:
            self.room_dropdown.add_widget(Button(
                text=room.name,
                size_hint_y=None,
                height=int(1/10 * self.app.root.height),
                on_release=partial(self.room_dropdown.select_, room)
            ))

        self.layout.add_widget(self.light_name)
        self.light_name.text = 'Enter light name'

        self.layout.add_widget(Button(
            text='Submit',
            on_release=self.submit
        ))

        self.layout.add_widget(Button(
            text='Cancel',
            on_release=self.dismiss
        ))

    def _form_is_valid(self) -> bool:
        return all((
          self.room_dropdown.selected_value,
          self.light_dropdown.selected_value,
          self.light_name.text
        ))

    def _do_form_actions(self):
        light = self.light_dropdown.selected_value
        room = self.room_dropdown.selected_value

        light.name = self.light_name.text
        room.add_light(light)

        app = App.get_running_app()
        app.on_edit_home()


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
