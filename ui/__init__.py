from utils.observer import Observer

# create frontend observer and register event types
events = Observer()
for event_name in ['set_controlled_lights', 'add_room']:
    events.register_event_name(event_name)
