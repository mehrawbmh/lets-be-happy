from app.models.schema import Schema


class UserUpdateSchema(Schema):
    username: str
    phone: str
    email: str | None = None
