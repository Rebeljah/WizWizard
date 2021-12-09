from typing import Type

from utils.observer import Observer

# create backend observer and register event types
events = Observer()

event_names = [
    'home_add_room', 'home_remove_room', 'add_light', 'remove_light',
    'light_set_wizlight',
]
for event_name in event_names:
    events.register_event_name(event_name)

# current home that is active in the app
active_home: Type['Home'] = None
