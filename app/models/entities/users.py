import re
from typing import NoReturn

from fastapi import HTTPException
from pydantic import Field, field_validator
from pymongo import ASCENDING
from starlette import status

from app.core.enum.roles import Role
from app.models.entity import Entity


class User(Entity):
    # id: str | None
    username: str
    password: str
    phone: str = Field(min_length=11, max_length=11)
    role: str = Role.USER
    email: str | None = Field(default=None)

    @staticmethod
    def get_collection_name():
        return 'users'

    @classmethod
    async def create_indexes(cls) -> NoReturn:
        collection = await cls.get_collection()
        await collection.create_index(
            [("username", ASCENDING)],
            name="username",
            unique=True,
            background=True,
        )

        await collection.create_index(
            [("email", ASCENDING)],
            name="email",
            unique=True,
            background=True,
        )

        await collection.create_index(
            [("phone", ASCENDING)],
            name="phone",
            unique=True,
            background=True,
        )

    @classmethod
    async def find_by_username(cls, username: str):
        collection = await cls.get_collection()
        db_data = await collection.find_one({"username": username})
        return cls._convert_document_to_object(db_data)

    @field_validator('email')
    def validate_email_regex(cls, email: str | None = None):
        if not email:
            return None

        email_pattern = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        if not re.fullmatch(email_pattern, email):
            # I suppose that all emails in all documents are in correct format already, and it's just while adding new
            raise HTTPException(status.HTTP_400_BAD_REQUEST, {'message': 'wrong email format!'})

        return email
