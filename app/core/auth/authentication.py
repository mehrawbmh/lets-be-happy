from fastapi import Depends

from models.entities.users import User
from dependencies.depends import get_main_db


# TODO: sanitize, escape or remove and error while getting injection with non-alphanumeric characters
class Authentication:
    @staticmethod
    def __check_password(user: User, given_password: str):
        return user.password == given_password

    async def find_user_by_username(self, username: str, db=Depends(get_main_db)) -> User:
        ...
