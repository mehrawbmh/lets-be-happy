from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.configs.settings import settings
from app.core.services.service import Service


class MongoClient(Service):
    """
    Mongo DB client and connection
    """
    __client: AsyncIOMotorClient | None = None
    __db: AsyncIOMotorDatabase | None = None

    @staticmethod
    async def __get_uri():
        username = getattr(settings, "MONGO_USERNAME", None)
        password = getattr(settings, "MONGO_PASSWORD", None)
        host_name = getattr(settings, "MONGO_HOST", 'localhost')
        port = getattr(settings, "MONGO_PORT", "27017")
        if username and password:  # it means there's auth!
            connection_uri = f"mongodb://{username}:{password}@{host_name}:27017/"
            # print('here MONGO using password')
        else:
            # print('here with NO AUTH MONGO')
            connection_uri = f"mongodb://{host_name}:27017/"
        return connection_uri

    @classmethod
    async def get_client(cls) -> AsyncIOMotorClient:
        return AsyncIOMotorClient(
            await cls.__get_uri(),
            serverSelectionTimeoutMS=10000
        )

    async def get_main_db(self) -> AsyncIOMotorDatabase:
        if self.__db is None:
            self.__client = await self.get_client() if not self.__client else self.__client

            dblist = await self.__client.list_database_names()
            if settings.MONGO_DB in dblist:
                self.__db = self.__client.get_database(settings.MONGO_DB)
            else:
                self.__db = self.__client[settings.MONGO_DB]
                # print("WARNING>>> creating DB!")
                await self.__db["init"].update_one({}, {"$set": {"OK": 1}}, upsert=True)

        return self.__db
