from models.base import Schema


class UserLogin(Schema):
    username: str
    password: str
