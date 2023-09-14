from app.models.base import Schema


class UserProfile(Schema):
    username: str
    email: str | None = None
    # TODO: which one is optional?!
    phone: str | None = None
