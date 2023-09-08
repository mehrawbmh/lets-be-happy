import re

from pydantic import Field, validator, field_validator

from models.base import Entity
from configs.roles import Role


class User(Entity):
    username: str
    password: str
    role: str = Role.USER
    email: str | None = Field(default=None)
    active: bool = True

    @field_validator(email)
    def validate_email_regex(self, email: str):
        email_pattern = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        return re.fullmatch(email_pattern, email)


