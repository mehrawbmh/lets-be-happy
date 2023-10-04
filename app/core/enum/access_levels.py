from enum import Enum

from app.core.enum.roles import Role


class AccessLevel(Enum):
    USER: list[str] = list(Role)
    ADMIN: list[str] = [Role.ADMIN, Role.SUPER_ADMIN]
    STAFF: list[str] = [Role.ADMIN, Role.STAFF, Role.SUPER_ADMIN]
    SUPER_ADMIN: list[str] = [Role.SUPER_ADMIN]
