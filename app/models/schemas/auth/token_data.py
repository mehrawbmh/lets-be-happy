from datetime import datetime

from app.core.enum.roles import Role
from app.models.schema import Schema


class UserTokenData(Schema):
    username: str | None = None
    id: str | None = None
    role: Role | None = None
    exp: datetime  # expiration time
