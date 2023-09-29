from datetime import datetime

from typing_extensions import Literal

from app.core.enum.task_priorities import TaskPriority
from app.core.enum.task_statuses import TaskStatus
from app.core.services.time_service import TimeService
from app.models.schema import Schema


class CreateTask(Schema):
    title: str
    assignee_username: str
    deadline: datetime = TimeService.get_today_end()
    status: Literal[TaskStatus.BACKLOG, TaskStatus.IN_PROGRESS] = TaskStatus.BACKLOG
    priority: TaskPriority = TaskPriority.MEDIUM
    description: str
