from model import Model


class User(Model):
    username: str
    password: str
    role: str
    email: str | None = None
    active: bool = True

