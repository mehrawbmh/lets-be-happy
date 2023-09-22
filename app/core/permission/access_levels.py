from enum import Enum

from app.configs.roles import Role


class AccessLevel(Enum):
    USER: list[str] = Role.ALL
    ADMIN: list[str] = [Role.ADMIN]
    STAFF: list[str] = [Role.ADMIN, Role.STAFF]
