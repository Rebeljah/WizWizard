
from typing import Callable
EventName = str
SubscriberDict = dict[EventName, set[Callable]]


class Observer:
    """Observer that runs subscribing callbacks when events are published"""
    def __init__(self):
        self.events: SubscriberDict = {}

        self.event_names = ['add_room', 'add_light', 'set_bulb']
        for event_name in self.event_names:
            self.add_event(event_name)

    def subscribe(self, event_name, callback):
        """Add the subscribing callback to the set of subscribers"""
        event_subscribers: set = self.events[event_name]
        event_subscribers.add(callback)

    def unsubscribe(self, event_name, callback):
        """remove the callback from the subscribers"""
        event_subscribers: set = self.events[event_name]
        event_subscribers.remove(callback)

    def publish(self, event_name, *callback_args):
        """Publish arguments to any callbacks subscribing to the event_name"""
        event_subscribers: set = self.events[event_name]
        for callback in event_subscribers:
            callback(*callback_args)

    def add_event(self, event_name):
        """Add event name to events dict"""
        assert event_name not in self.events
        self.events.update({event_name: set()})

    def del_event(self, event_name):
        del self.events[event_name]
