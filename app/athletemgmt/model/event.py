from dojocommons.model.base_event import BaseEvent

from athletemgmt.model.resource import Resource


class Event(BaseEvent):
    resource: str
