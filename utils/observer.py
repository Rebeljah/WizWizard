"""Observer  that allows the backend to subscribe to UI events and visa-versa"""


from typing import Callable
EventName = str
SubscriberDict = dict[EventName, set[Callable]]


class Observer:
    """Observer that runs subscribing callbacks when events are published"""
    def __init__(self):
        self.subscriber_dict: SubscriberDict = {}

    def subscribe(self, event_name, *callbacks):
        """Add the subscribing callback to the set of subscribers"""
        subscribers: set = self.subscriber_dict[event_name]
        for cb in callbacks:
            subscribers.add(cb)

    def unsubscribe(self, event_name, callback):
        """remove the callback from the subscribers"""
        subscribers: set = self.subscriber_dict[event_name]
        subscribers.remove(callback)

    def publish(self, event_name, *args):
        """Publish arguments to any callbacks subscribing to the event_name"""
        subscribers: set = self.subscriber_dict[event_name]
        for callback in subscribers:
            callback(*args)

    def add_event_name(self, event_name):
        """Add event name to events dict"""
        assert event_name not in self.subscriber_dict
        self.subscriber_dict.update({event_name: set()})

    def del_event(self, event_name):
        del self.subscriber_dict[event_name]
