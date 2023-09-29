from enum import Enum


class EventTypes(str, Enum):
    STARTUP: str = "startup"
    SHUTDOWN: str = "shutdown"
