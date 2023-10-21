from datetime import datetime

from app.core.enum.task_priorities import TaskPriority
from app.core.enum.task_statuses import TaskStatus
from app.models.schema import Schema


class TaskUpdateSchema(Schema):
    title: str
    assignee: str
    deadline: datetime
    status: TaskStatus
    priority: TaskPriority
    description: str
