from enum import Enum


class Role(str, Enum):
    ADMIN: str = 'admin'
    USER: str = 'user'
    STAFF: str = 'staff'
