from pydantic import BaseModel


class Schema(BaseModel):
    """
        This should be for models which aren't DB documents, but just schemas used on non-db layers.
        You have to specify use case when you want to add schema. e.g: there's just one user entity, but it can contain
        multiple user schemas on different purposes: UserLogin, UserSignUp, etc.
    """
    pass
