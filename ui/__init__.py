from utils.observer import Observer, EventBase


class SetSelectedLights(EventBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class AddRoom(EventBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


# create frontend observer and register event types
events = Observer()
for event_type in [SetSelectedLights, AddRoom]:
    events.register_event_type(event_type)
