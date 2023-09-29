from abc import ABC, abstractmethod
from typing import Self

from bson import ObjectId
from bson.errors import InvalidId
from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorDatabase
from pydantic import BaseModel, Field
from pymongo.results import InsertOneResult

from app.core.services.response_service import responseService
from app.core.services.time_service import TimeService
from app.dependencies.database import get_main_db


class Entity(BaseModel, ABC):
    """
        This is for models which are DB documents (same as SQL tables) -  all entities of our application
        todo: add orm methods and stuff to it + getter setters
    """
    id: str | None = None
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
    def create_object_id(cls, document_id: str):
        try:
            return ObjectId(document_id)
        except InvalidId:
            return False  # TODO: take other actions?

    @classmethod
    async def find_by_id(cls, document_id: str, allow_none: bool = True,
                         not_found_error_message: str = 'invalid id provided.') -> Self | None:
        collection = await cls.get_collection()
        db_data = await collection.find_one({"_id": cls.create_object_id(document_id)})

        if (not db_data) and (not allow_none):
            return responseService.error_404(not_found_error_message)

        return cls.model_validate({**db_data, 'id': str(db_data['_id'])}) if db_data else None

    @classmethod
    async def list_find_many(cls, condition: dict, max_length: int = 1000) -> list[Self]:
        collection = await cls.get_collection()
        documents = await collection.find(condition).to_list(max_length)
        return list(map(lambda doc: cls._convert_document_to_object(doc), documents))

    async def insert(self, exclude: set | None = None) -> InsertOneResult:
        exclude = exclude if exclude else set()
        exclude.add('id')
        collection = await self.get_collection()
        return await collection.insert_one(self.model_dump(exclude=exclude))

    @classmethod
    def _convert_document_to_object(cls, db_data: dict | None) -> Self:
        return cls.model_validate({**db_data, 'id': str(db_data['_id'])}) if db_data else None
