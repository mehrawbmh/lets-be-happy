from jose import jwt
from configs.settings import settings
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta

from models.schemas.auth.token_data import TokenData


class JWTAuthentication:
    password_context = CryptContext(schemes=['bcrypt'])
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

    def __init__(self, token: str | None = None):
        self.token = token

    def get_user(self):


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
