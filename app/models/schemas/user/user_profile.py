from app.core.enum.roles import Role
from app.models.schema import Schema


class UserProfile(Schema):
    username: str
    email: str | None = None
    # TODO: which one is optional?!
    phone: str | None = None
    role: Role
