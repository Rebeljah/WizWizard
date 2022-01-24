"""Observer  that allows the backend to subscribe to UI events and visa-versa"""


from typing import Callable, Type
EventName = str


class EventBase:
    def __init__(self, **kwargs):
        self.kwargs = kwargs


class Observer:
    """Observer that runs subscribing callbacks when events are published"""
    def __init__(self):
        self.subscriber_dict: dict[Type[EventBase], set[Callable]] = {}

    def subscribe(self, event_type: Type[EventBase], callback: Callable):
        """Add the subscribing callback to the set of subscribers"""
        self.subscriber_dict[event_type].add(callback)

    def publish(self, event: EventBase):
        """Publish arguments to any callback routines subscribing to the event_name"""
        event_type = type(event)
        subscribers = self.subscriber_dict[event_type]
        for callback in subscribers:
            callback(**event.kwargs)

    def register_event_type(self, event_type: Type[EventBase]):
        """Add event name to events dict"""
        assert event_type not in self.subscriber_dict
        self.subscriber_dict[event_type] = set()
