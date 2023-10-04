from pydantic import Field

from app.core.enum.roles import Role
from app.models.schema import Schema


class LoginResponse(Schema):
    access_token: str
    token_type: str
    success: bool = Field(default=True)
    role: Role
