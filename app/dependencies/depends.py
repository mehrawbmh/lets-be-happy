from fastapi import Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from core.mongo import MongoClient
from models.entities.users import User
from fastapi.security import OAuth2PasswordBearer


async def get_main_db() -> AsyncIOMotorDatabase:
    """
    :return: MongoDB database
    """
    client = MongoClient()
    return await client.get_main_db()


async def get_current_user(token: str = Depends(OAuth2PasswordBearer("jwt_token"))) -> User:
    """
   :return: current user based on request header token
   """
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not logged in yet",
        )
