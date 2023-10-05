from abc import ABC

from app.models.model import Model


class Schema(Model, ABC):
    """
        This should be for models which aren't DB documents, but just schemas used on non-db layers.
        You have to specify use case when you want to add schema. e.g: there's just one user entity, but it can contain
        multiple user schemas on different purposes: UserLogin, UserSignUp, etc.
    """

    class Config:
        pass
