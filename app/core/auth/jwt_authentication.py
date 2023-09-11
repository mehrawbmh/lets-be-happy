from jose import jwt, JWTError, ExpiredSignatureError
from configs.settings import settings
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi.exceptions import HTTPException
from fastapi import status
from datetime import datetime, timedelta

from models.entities.users import User
from models.schemas.auth.token_data import TokenData


class JWTAuthentication:
    password_context = CryptContext(schemes=['bcrypt'])
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

    def __init__(self, token: str | None = None):
        self.token = token

    def get_user(self):
        if not self.token:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, {"message": "You have to log in first!"})
        try:
            user_data = self.decode()
        except ExpiredSignatureError:
            #TODO: redirect
            return
        except JWTError:
            raise HTTPException(status.HTTP_403_FORBIDDEN, {"message": "Wrong login token given"})

        user_data = TokenData.model_validate(user_data)
        return User.find_by_username(user_data.username)

    @classmethod
    def hash_password(cls, plain_password: str):
        return cls.password_context.hash(plain_password)

    def check_password(self, plain: str, hashed: str) -> bool:
        return self.password_context.verify(plain, hashed)

    @staticmethod
    def encode(data: TokenData, expiration_seconds: int = settings.ACCESS_TOKEN_EXPIRATION_SECONDS):
        to_encode_data = data.model_dump()
        to_encode_data["exp"] = datetime.utcnow() + timedelta(seconds=expiration_seconds)
        return jwt.encode(to_encode_data, settings.SECRET_KEY, settings.AUTHORIZATION_HASH_ALGORITHM)

    def decode(self) -> dict:
        return jwt.decode(self.token, settings.SECRET_KEY, settings.AUTHORIZATION_HASH_ALGORITHM)
