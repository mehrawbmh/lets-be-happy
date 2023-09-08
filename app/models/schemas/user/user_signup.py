from pydantic import Field

from models.base import Schema


class UserSignUp(Schema):
    username: str
    password: str
    email: str | None = None
