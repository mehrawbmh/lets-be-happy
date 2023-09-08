from models.base import Schema


class Token(Schema):
    access_token: str
    token_type: str
