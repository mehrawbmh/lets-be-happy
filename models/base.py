from pydantic import BaseModel


class Entity(BaseModel):
    """
        This is for models which are DB documents (same as SQL tables) -  all entities of our application
        todo: add orm methods and stuff to it + getter setters
    """
    pass


class Schema(BaseModel):
    """
        This should be for models which aren't DB documents, but just schemas used on non-db layers.
        You have to specify use case when you want to add schema. e.g: there's just one user entity, but it can contain
        multiple user schemas on different purposes: UserLogin, UserSignUp, etc.
    """
    pass

# FIXME: is it better to put them not together but in their own directory? better importing and cleaner...
