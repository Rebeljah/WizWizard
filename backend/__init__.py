
from typing import Type

from utils.observer import Observer, EventBase


class HomeAddRoom(EventBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class HomeRemoveRoom(EventBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class AddLight(EventBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class RemoveLight(EventBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class LightSetWizlight(EventBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


# create backend observer and register event types
events = Observer()

event_types = [
    HomeAddRoom, HomeRemoveRoom, AddLight, RemoveLight, LightSetWizlight
]
for event_type in event_types:
    events.register_event_type(event_type)

# current home that is active in the app
active_home: Type['Home'] = None
