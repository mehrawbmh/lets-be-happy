# TODO: make it singleton
from pathlib import Path

from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    class Config:
        """
        Config .env file for project credential and environment stuff
        """
        env_file = '.env'
        env_file_encoding = 'utf-8'
        fields_list = ['SECRET_KEY', 'MONGO_HOST', 'MONGO_USERNAME', 'MONGO_PORT', 'MONGO_PASSWORD', 'MONGO_DB']
        fields = {item: {'env': item} for item in fields_list}

    MONGO_USERNAME = ""
    MONGO_PASSWORD = ""
    MONGO_DB = "main"
    MONGO_PORT = "27017"
    MONGO_HOST = "localhost"

    BASE_DIR = str(Path(__file__).resolve().parent.parent)
    PROJECT_NAME = str("lets-be-happy")

    SECRET_KEY = str()
    AUTHORIZATION_HASH_ALGORITHM = str()
    ACCESS_TOKEN_EXPIRATION_SECONDS = 48 * 60 * 60


settings = Settings()
