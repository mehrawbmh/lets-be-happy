import re
from typing import NoReturn

from pydantic import Field, field_validator, ValidationInfo
from pymongo import ASCENDING

from app.core.enum.roles import Role
from app.core.services.response_service import responseService
from app.models.entity import Entity


class User(Entity):
    # id: str | None
    username: str
    password: str
    phone: str = Field()
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

    @field_validator('username')
    @classmethod
    def check_alphanumeric(cls, field: str, info: ValidationInfo) -> str:
        if isinstance(field, str):
            if not (field.isalnum() and field.isascii()):
                return responseService.error_400(f"{info.field_name} must be english alphanumeric!")

        return field

    @field_validator('email')
    @classmethod
    def validate_email_regex(cls, email: str | None, info: ValidationInfo):
        if not email:
            return None

        email_pattern = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        if not re.fullmatch(email_pattern, email):
            # I suppose that all emails in all documents are in correct format already, and it's just while adding new
            return responseService.error_400('wrong email format!')

        return email

    @field_validator('phone')
    @classmethod
    def validate_phone_number(cls, phone: str, info: ValidationInfo):
        if phone.startswith('09') and len(phone) == 11:
            return phone

        return responseService.error_400('bad phone nubmer given')

    @classmethod
    def check_raw_password(cls, password: str):
        if not cls.is_password_valid(password):
            return responseService.error_400(
                "invalid password given." +
                "password must be at least 8 characters and " +
                "contain at least one lower and one upper case letter, one digit and one special character " +
                "( - @ _ # )"
            )

    @staticmethod
    def is_password_valid(password: str) -> bool:
        special_chars = ['@', '$', '_', '-']
        lower_count, upper_count, special_char_count, digit_count = 0, 0, 0, 0

        if len(password) >= 8:
            for char in password:
                lower_count += int(char.islower())
                upper_count += int(char.isupper())
                digit_count += int(char.isdigit())
                special_char_count += int(char in special_chars)

        checks = [lower_count, upper_count, digit_count, special_char_count]
        return all(checks) and sum(checks) == len(password)
