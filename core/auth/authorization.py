from jose import jwt, JWTError, ExpiredSignatureError
from configs.settings import settings


class Authorization:
    def __init__(self, token: str | None = None):
        self.token = token

    @property
    def is_token_valid(self):
        try:
            token_data = jwt.decode(self.token, settings.SECRET_KEY)
        except ExpiredSignatureError:
            ...
        except JWTError:
            ...
