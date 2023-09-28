from fastapi import Depends, APIRouter
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.dependencies.database import get_main_db
from app.dependencies.user import get_staff_user
from app.models.entities.users import User
from app.models.schemas.task.task_create import CreateTask

router = APIRouter(prefix='/tasks')


@router.post('/tasks/create')
async def create_task(task_input: CreateTask, user: User = Depends(get_staff_user),
                      db: AsyncIOMotorDatabase = Depends(get_main_db)):
    print(task_input.model_dump())
    return {'ok': 1}
    # task: Task = Task.model_validate(task_input.model_dump())
