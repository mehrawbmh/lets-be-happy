from datetime import datetime, date

from pydantic import Field

from app.core.enum.task_priorities import TaskPriority
from app.core.enum.task_statuses import TaskStatus
from app.models.base import Entity


class Task(Entity):
    @staticmethod
    def get_collection_name():
        return 'tasks'

    created_by: str  # user id
    assigned_to: str  # user id
    deadline: date
    finished_at: datetime | None
    status: TaskStatus = TaskStatus.BACKLOG
    priority: TaskPriority
    description: str = Field(default='')
