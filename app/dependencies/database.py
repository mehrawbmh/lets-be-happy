from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.database.mongo import MongoClient


async def get_main_db() -> AsyncIOMotorDatabase:
    """
    :return: MongoDB database
    """
    client = MongoClient()
    return await client.get_main_db()
