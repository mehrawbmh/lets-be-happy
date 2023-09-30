from typing import NoReturn

from app.models.entity import Entity


class DatabaseIndexManager:
    @staticmethod
    async def crete_indexes() -> NoReturn:
        """
        Create proper indexes for each entity if not exist
        """

        for entity in Entity.__subclasses__():
            await entity.create_indexes()

        print("indexes were created successfully")
