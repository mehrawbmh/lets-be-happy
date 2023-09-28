from datetime import datetime

from typing_extensions import Literal

from app.core.enum.task_priorities import TaskPriority
from app.core.services.time_service import TimeService
from app.models.schema import Schema


class CreateTask(Schema):
    assignee_username: str
    deadline: datetime = TimeService.get_today_end()
    finished_at: datetime | None = None
    priority: TaskPriority = TaskPriority.MEDIUM
    description: str
    saf: Literal['aa'] = 'aa'
