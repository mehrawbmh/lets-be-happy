from pydantic import Field

from app.models.schema import Schema


class Token(Schema):
    access_token: str
    token_type: str
    success: bool = Field(default=True)
