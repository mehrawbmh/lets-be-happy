from typing import Self

from pydantic import model_validator

from app.core.services.response_service import responseService
from app.models.schema import Schema


class ChangePassword(Schema):
    old_password: str
    new_password: str
    new_password_repeat: str

    class Config:
        hide_input_in_errors = True

    @model_validator(mode='after')
    def check_passwords_match(self) -> Self:
        if self.new_password != self.new_password_repeat:
            return responseService.error_400('passwords do not match')
        if self.new_password == self.old_password:
            return responseService.error_400('you have to choose new password')

        return self
