from enum import Enum


class Role(str, Enum):
    SUPER_ADMIN: str = 'super_admin'
    ADMIN: str = 'admin'
    USER: str = 'user'
    STAFF: str = 'staff'
