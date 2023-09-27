from pydantic import Field

from app.models.schema import Schema


class UserSignUp(Schema):
    username: str
    password: str
    phone: str = Field(min_length=11, max_length=11)
    email: str | None = None
