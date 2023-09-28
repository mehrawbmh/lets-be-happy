from enum import Enum


class TaskStatus(str, Enum):
    BACKLOG: str = 'backlog'
    INVALID: str = 'invalid'
    DONE: str = 'done'
    IN_PROGRESS: str = 'in-progress'
    BLOCKED: str = 'blocked'
