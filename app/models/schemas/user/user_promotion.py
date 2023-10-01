from app.core.enum.roles import Role
from app.models.schema import Schema


class UserPromoteSchema(Schema):
    username: str
    new_role: Role
