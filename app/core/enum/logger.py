from enum import Enum


class Logger(str, Enum):
    DEFAULT = 'default logger'
    STARTUP = 'start up events'
