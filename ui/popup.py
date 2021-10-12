from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button


def show_notification(title: str) -> None:
    """Open a popup window with the given title"""
    content = FloatLayout()
    popup = Popup(title=title, content=content, size_hint=(.25, .25))

    dismiss_button = Button(
        text='ok',
        on_release=popup.dismiss,
        size_hint=(.2, .1),
        pos_hint={'center_x': .5, 'center_y': .5}
    )
    content.add_widget(dismiss_button)

    popup.open()
