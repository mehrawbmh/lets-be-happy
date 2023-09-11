from enum import Enum


class Role(Enum):
    ADMIN: str = 'admin'
    USER: str = 'user'
    STAFF: str = 'staff'
