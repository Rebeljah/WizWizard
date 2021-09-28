from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.app import App


class NavBar(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # formatting
        self.cols = 2
        self.size_hint_y = 0.2
        self.padding = 10

        self.build()

    def build(self):
        self.clear_widgets()
        self.add_widget(self.RoomNavbar())
        self.add_widget(self.AddRoomButton())

    class RoomNavbar(GridLayout):
        """Grid layout to hold room buttons"""
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.app: App = App.get_running_app()

            self.cols = 7
            self.rows = 1

            self.build()

        def build(self) -> None:
            # add buttons for rooms
            for room in self.app.home.rooms:
                self.add_widget(self.RoomNavButton(room.name, room.id))

        class RoomNavButton(Button):
            """A button for selecting the room to control lights in"""
            def __init__(self, room_name: str, room_id: str, **kwargs):
                super().__init__(**kwargs)
                self.app = App.get_running_app()

                # store the room name and id
                self.room_name = room_name
                self.room_id: str = room_id

                # button formatting
                self.text = self.room_name
                self.on_release = self.show_room

            def show_room(self):
                """Set room controls page to this room using the room id"""
                self.app.set_current_room(self.room_id)

    class AddRoomButton(Button):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.app = App.get_running_app()

            self.text = '+ Add room'
            self.size_hint = 0.2, 0.2
            self.on_release = self.app.add_room_form.open
