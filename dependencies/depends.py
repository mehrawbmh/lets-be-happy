from fastapi import Depends, HTTPException, status, Request, Body
from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi.security import OAuth2PasswordRequestForm

from clients.mongo import MongoClient


async def get_main_db() -> AsyncIOMotorDatabase:
    """
    :return: MongoDB database
    """
    client = MongoClient()
    return await client.get_main_db()
