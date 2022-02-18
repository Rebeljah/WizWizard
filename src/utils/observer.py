"""Observer  that allows the backend to subscribe to UI events and visa-versa"""

from enum import Enum, auto
from typing import Callable


class Event(Enum):
    AddedRoom = auto()
    RemovedRoom = auto()
    EditedRoom = auto()
    AddedLight = auto()
    RemovedLight = auto()
    UpdatedLight = auto()
    SetControlledLights = auto()


class Observer:
    """Observer that runs subscribing callbacks when events are published"""
    def __init__(self):
        self.subscriber_dict: dict[Event, set[Callable]] = {}
        for event_enum in Event:
            self._register_event_type(event_enum)

    def subscribe(self, event: Event, callback: Callable):
        """Add the subscribing callback to the set of subscribers"""
        self.subscriber_dict[event].add(callback)

    def publish(self, event: Event, *args, **kwargs):
        """Publish arguments to any callback routines subscribing to the event_name"""
        subscribers = self.subscriber_dict[event]
        for callback in subscribers:
            callback(*args, **kwargs)

    def _register_event_type(self, event: Event):
        """Add event name to events dict"""
        assert event not in self.subscriber_dict
        self.subscriber_dict[event] = set()
