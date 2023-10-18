from enum import Enum


class LogSection(str, Enum):
    DEFAULT = 'default logger'
    STARTUP = 'start up events'
