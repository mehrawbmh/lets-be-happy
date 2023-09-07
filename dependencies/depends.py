from fastapi import Depends, HTTPException, status, Request, Body
from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi.security import OAuth2PasswordRequestForm


def get_main_db() -> AsyncIOMotorDatabase:
    """
    :return: MongoDB database
    """
    ...
