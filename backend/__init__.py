
from typing import Type

from observer.observer import Observer

# create backend observer and register event types
events = Observer()
for event_name in ['add_room', 'add_light', 'update_light']:
    events.add_event_name(event_name)

# current home that is active in the app
active_home: Type['Home'] = None
