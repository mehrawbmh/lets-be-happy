from enum import StrEnum


class Role(StrEnum):
    ADMIN: str = 'admin'
    USER: str = 'user'
    STAFF: str = 'staff'
