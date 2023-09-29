from enum import Enum


class Tags(str, Enum):
    USER = 'user'
    AUTH = 'authentication'
    TASK = 'task'
