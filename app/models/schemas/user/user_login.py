from app.models.schema import Schema


class UserLogin(Schema):
    username: str
    password: str
