from datetime import datetime
from typing import NoReturn

from pydantic import Field
from pymongo import ASCENDING, DESCENDING

from app.core.enum.task_priorities import TaskPriority
from app.core.enum.task_statuses import TaskStatus
from app.models.entity import Entity


class Task(Entity):
    @staticmethod
    def get_collection_name():
        return 'tasks'

    @classmethod
    async def create_indexes(cls) -> NoReturn:
        collection = await cls.get_collection()
        await collection.create_index(
            [("assignee", ASCENDING), ("deadline", DESCENDING)],
            name="assignee_deadline",
            background=True
        )

    title: str
    created_by: str  # username # TODO: is it better idea to change it to user id?!
    assignee: str  # username
    deadline: datetime
    finished_at: datetime | None = None
    status: TaskStatus = TaskStatus.BACKLOG
    priority: TaskPriority
    description: str = Field(default='')
