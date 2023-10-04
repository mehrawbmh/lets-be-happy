from fastapi import HTTPException, status

from app.core.enum.access_levels import AccessLevel
from app.models.schemas.auth.token_data import UserTokenData


class PermissionManager:
    def __init__(self, user: UserTokenData | None = None):
        self.user = user

    def permit(self, access_level: AccessLevel):
        if self.user and self.user.role in access_level.value:
            return
        raise HTTPException(status.HTTP_403_FORBIDDEN, {'message': 'You are not allowed to see this page'})
