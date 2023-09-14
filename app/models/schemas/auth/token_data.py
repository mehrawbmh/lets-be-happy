from app.models.base import Schema


class TokenData(Schema):
    username: str | None = None
    id: str | None = None
