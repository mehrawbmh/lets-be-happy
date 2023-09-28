from fastapi import HTTPException, status

from app.core.enum.access_levels import AccessLevel
from app.models.entities.users import User


class PermissionManager:
    def __init__(self, user: User | None = None):
        self.user = user

    def permit(self, access_level: AccessLevel):
        if self.user and self.user.role in access_level.value:
            return
        raise HTTPException(status.HTTP_403_FORBIDDEN, {'message': 'You are not allowed to see this page'})