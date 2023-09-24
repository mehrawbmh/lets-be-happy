from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.auth.jwt_authentication import JWTAuthentication
from app.core.enum.access_levels import AccessLevel
from app.core.permission.permission_manager import PermissionManager
from app.models.entities.users import User


async def get_token(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())) -> str:
    """
     :return: token given in request header if it's bearer, else empty string
     """
    return credentials.credentials if credentials.scheme == "Bearer" else ""


async def get_current_user(token: str = Depends(get_token)) -> User:
    """
   :return: current user based on request header token
   """
    if user := await JWTAuthentication(token).get_user():
        return user

    raise HTTPException(status.HTTP_404_NOT_FOUND, {'message': 'user id in token not found!'})


async def get_admin_user(user: User = Depends(get_current_user)):
    PermissionManager(user).permit(AccessLevel.ADMIN)
    return user


async def get_staff_user(user: User = Depends(get_current_user)):
    PermissionManager(user).permit(AccessLevel.STAFF)
