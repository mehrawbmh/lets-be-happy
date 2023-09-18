from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.auth.jwt_authentication import JWTAuthentication
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

    raise HTTPException(status.HTTP_404_NOT_FOUND, 'user id in token not found!')
