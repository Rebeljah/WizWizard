
from typing import Type

from utils.observer import Observer

# create backend observer and register event types
events = Observer()

events_names = [
    'home_add_room', 'home_remove_room', 'add_light', 'remove_light',
    'light_set_wizlight',
]
for event_name in events_names:
    events.add_event_name(event_name)

# current home that is active in the app
active_home: Type['Home'] = None
