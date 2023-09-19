from datetime import datetime, timedelta

from fastapi import status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError, ExpiredSignatureError
from passlib.context import CryptContext

from app.configs.settings import settings
from app.models.entities.users import User
from app.models.schemas.auth.token import Token
from app.models.schemas.auth.token_data import TokenData


class JWTAuthentication:
    password_context = CryptContext(schemes=['bcrypt'])
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

    def __init__(self, token: str | None = None):
        self.token = token

    async def login_with_password(self, username: str, password: str) -> Token:
        user = await User.find_by_username(username)

        if user and self.check_password(password, user.password):
            user_data = TokenData.model_validate(user.model_dump())
            bearer_token = self.encode(user_data)
            return Token(access_token=bearer_token, token_type="Bearer")

        raise HTTPException(status.HTTP_403_FORBIDDEN, {"message": "invalid username or password"})

    def get_user(self):
        if not self.token:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, {"message": "You have to log in first!"})
        try:
            user_data = self.decode()
        except ExpiredSignatureError:
            # TODO: redirect
            return
        except JWTError:
            raise HTTPException(status.HTTP_403_FORBIDDEN, {"message": "Wrong login token given"})

        user_data = TokenData.model_validate(user_data)
        return User.find_by_id(user_data.id)

    @classmethod
    def hash_password(cls, plain_password: str):
        return cls.password_context.hash(plain_password)

    def check_password(self, plain: str, hashed: str) -> bool:
        return self.password_context.verify(plain, hashed)

    @staticmethod
    def encode(data: TokenData, expiration_seconds: int = settings.ACCESS_TOKEN_EXPIRATION_SECONDS) -> str:
        to_encode_data = data.model_dump()
        to_encode_data["exp"] = datetime.utcnow() + timedelta(seconds=expiration_seconds)
        return jwt.encode(to_encode_data, settings.SECRET_KEY, settings.AUTHORIZATION_HASH_ALGORITHM)

    def decode(self) -> dict:
        return jwt.decode(self.token, settings.SECRET_KEY, settings.AUTHORIZATION_HASH_ALGORITHM)
