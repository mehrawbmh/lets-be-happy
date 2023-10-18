from typing import NoReturn

from app.core.enum.log_sections import LogSection
from app.core.services.log_service import logService
from app.models.entity import Entity


class DatabaseIndexManager:
    @staticmethod
    async def crete_indexes() -> NoReturn:
        """
        Create proper indexes for each entity if not exist
        """

        for entity in Entity.__subclasses__():
            await entity.create_indexes()

        logService.get_logger(LogSection.STARTUP).info('db indexes created successfully.')
