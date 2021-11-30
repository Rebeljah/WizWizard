from utils.observer import Observer

# create backend observer and register event types
events = Observer()

events_names = [
    'add_room', 'remove_room', 'add_light', 'update_light'
]
for event_name in events_names:
    events.add_event_name(event_name)
