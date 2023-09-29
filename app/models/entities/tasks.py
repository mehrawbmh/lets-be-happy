from datetime import datetime

from pydantic import Field

from app.core.enum.task_priorities import TaskPriority
from app.core.enum.task_statuses import TaskStatus
from app.models.entity import Entity


class Task(Entity):
    @staticmethod
    def get_collection_name():
        return 'tasks'

    created_by: str  # username # TODO: is it better idea to change it to user id?!
    assignee: str  # username
    deadline: datetime
    finished_at: datetime | None = None
    status: TaskStatus = TaskStatus.BACKLOG
    priority: TaskPriority
    description: str = Field(default='')
