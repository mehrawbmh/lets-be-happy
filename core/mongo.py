from configs.settings import settings
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase


# TODO: make it singleton
class MongoClient:
    """
    Mongo DB client and connection
    """
    __client: AsyncIOMotorClient | None = None
    __db: AsyncIOMotorDatabase | None = None

    @staticmethod
    async def __get_uri():
        username = getattr(settings, "MONGO_USERNAME", None)
        password = getattr(settings, "MONGO_PASSWORD", None)
        host_name = getattr(settings, "MONGO_HOST", "")
        port = getattr(settings, "MONGO_PORT", "")

        if password:  # it means there's auth!
            connection_uri = f"mongodb://{username}:{password}@{host_name}:{port}/{settings.MONGO_DB}"
        else:
            connection_uri = f"mongodb://{host_name}:{port}/{settings.MONGO_DB}"

        return connection_uri

    @classmethod
    async def get_client(cls) -> AsyncIOMotorClient:
        return AsyncIOMotorClient(
            await cls.__get_uri(),
            serverSelectionTimeoutMS=3000
        )

    async def get_main_db(self) -> AsyncIOMotorDatabase:
        if not self.__db:
            self.__client = await self.get_client() if not self.__client else self.__client
            dblist = await self.__client.list_database_names()

            if settings.MONGO_DB in dblist:
                self.__db = self.__client.get_database(settings.MONGO_DB)
                return self.__db

            raise Exception("Database not found!!")  # TODO: make it connectionException or something like that

        return self.__db
