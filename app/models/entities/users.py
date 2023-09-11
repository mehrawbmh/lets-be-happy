import re

from pydantic import Field, field_validator

from configs.roles import Role
from dependencies.database import get_main_db
from models.base import Entity


class User(Entity):
    # TODO: add id?
    id: str
    username: str
    password: str
    role: str = Role.USER
    email: str | None = Field(default=None)
    active: bool = True

    @classmethod
    async def find_by_username(cls, username: str):
        db = await get_main_db()  # TODO: find better way to inject db here
        db_data = await db.users.find_one({"username": username})

        return cls.model_validate({**db_data, 'id': str(db_data['_id'])}) if db_data else None

    @field_validator('email')
    def validate_email_regex(cls, email: str | None = None):
        if email is None:
            return

        email_pattern = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        return re.fullmatch(email_pattern, email)
