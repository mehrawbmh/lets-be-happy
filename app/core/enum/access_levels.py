from enum import Enum

from app.core.enum.roles import Role


class AccessLevel(Enum):
    USER: list[str] = list(Role)
    ADMIN: list[str] = [Role.ADMIN]
    STAFF: list[str] = [Role.ADMIN, Role.STAFF]
