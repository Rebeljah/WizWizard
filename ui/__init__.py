from observer.observer import Observer

# create frontend observer and register event types
events = Observer()
for event_name in ['set_controlled_lights']:
    events.add_event_name(event_name)
