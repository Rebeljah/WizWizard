"""Observer  that allows the backend to subscribe to UI events and visa-versa"""


from typing import Callable
EventName = str
CallBackTuple = tuple[Callable]
SubscriberDict = dict[EventName, set[CallBackTuple]]


class Observer:
    """Observer that runs subscribing callbacks when events are published"""
    def __init__(self):
        self.subscriber_dict: SubscriberDict = {}

    def subscribe(self, event_name, *callbacks):
        """Add the subscribing callback to the set of subscribers"""
        subscribers: set[tuple] = self.subscriber_dict[event_name]
        subscribers.add(callbacks)

    def publish(self, event_name, *args):
        """Publish arguments to any callback routines subscribing to the event_name"""
        subscribers: set = self.subscriber_dict[event_name]
        for callback_routine in subscribers:
            for callback in callback_routine:
                callback(*args)

    def register_event_name(self, event_name):
        """Add event name to events dict"""
        assert event_name not in self.subscriber_dict
        self.subscriber_dict.update({event_name: set()})

    def del_event(self, event_name):
        del self.subscriber_dict[event_name]
