from abc import ABC, abstractmethod
from typing import Self

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorDatabase
from pydantic import BaseModel, Field
from pymongo.results import InsertOneResult

from app.core.services.time_service import TimeService
from app.dependencies.database import get_main_db


class Entity(BaseModel, ABC):
    """
        This is for models which are DB documents (same as SQL tables) -  all entities of our application
        todo: add orm methods and stuff to it + getter setters
    """
    id: str | None
    active: bool = True
    created_at: str = Field(default=str(TimeService.get_now()))

    @staticmethod
    @abstractmethod
    def get_collection_name():
        raise NotImplementedError('You must implement this method!!')

    @staticmethod
    async def get_db() -> AsyncIOMotorDatabase:
        return await get_main_db()

    @classmethod
    async def get_collection(cls) -> AsyncIOMotorCollection:
        db = await cls.get_db()
        return db[cls.get_collection_name()]

    @classmethod
    async def find_by_id(cls, document_id: str):
        collection = await cls.get_collection()
        db_data = await collection.find_one({"_id": ObjectId(document_id)})

        return cls.model_validate({**db_data, 'id': str(db_data['_id'])}) if db_data else None

    @classmethod
    async def find_many(cls, condition: dict, max_length: int = 1000):
        collection = await cls.get_collection()
        return await collection.find(condition).to_list(max_length)

    async def insert(self, exclude: set | None = None) -> InsertOneResult:
        exclude = exclude if exclude else set()
        exclude.add('id')
        collection = await self.get_collection()
        return await collection.insert_one(self.model_dump(exclude=exclude))

    @classmethod
    def _convert_document_to_object(cls, db_data: dict | None) -> Self:
        return cls.model_validate({**db_data, 'id': str(db_data['_id'])}) if db_data else None


class Schema(BaseModel):
    """
        This should be for models which aren't DB documents, but just schemas used on non-db layers.
        You have to specify use case when you want to add schema. e.g: there's just one user entity, but it can contain
        multiple user schemas on different purposes: UserLogin, UserSignUp, etc.
    """
    pass

# FIXME: is it better to put them not together but in their own directory? better importing and cleaner...
