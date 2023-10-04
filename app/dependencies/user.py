from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.auth.jwt_authentication import JWTAuthentication
from app.core.enum.access_levels import AccessLevel
from app.core.permission.permission_manager import PermissionManager
from app.models.schemas.auth.token_data import TokenData


async def get_token(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())) -> str:
    """
     :return: token given in request header if it's bearer, else empty string
     """
    return credentials.credentials if credentials.scheme == "Bearer" else ""


async def get_current_user(token: str = Depends(get_token)) -> TokenData:
    """
   :return: current user based on request header token
   """
    if user := JWTAuthentication(token).get_user():
        return user

    raise HTTPException(status.HTTP_404_NOT_FOUND, {'message': 'user id in token not found!'})


async def get_admin_user(user: TokenData = Depends(get_current_user)):
    PermissionManager(user).permit(AccessLevel.ADMIN)
    return user


async def get_staff_user(user: TokenData = Depends(get_current_user)):
    PermissionManager(user).permit(AccessLevel.STAFF)
    return user


async def get_super_admin_user(user: TokenData = Depends(get_current_user)):
    PermissionManager(user).permit(AccessLevel.SUPER_ADMIN)
