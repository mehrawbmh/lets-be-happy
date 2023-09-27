from app.models.schema import Schema


class TokenData(Schema):
    username: str | None = None
    id: str | None = None
