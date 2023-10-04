from app.core.enum.roles import Role
from app.models.schema import Schema


class TokenData(Schema):
    username: str | None = None
    id: str | None = None
    role: Role | None = None
    exp: int  # expiration time
