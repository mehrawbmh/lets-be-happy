from fastapi import Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from core.mongo import MongoClient
from models.entities.users import User
from core.auth.jwt_authentication import JWTAuthentication
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
    return JWTAuthentication(token).get_user()
