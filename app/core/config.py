from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    ASYNC_DATABASE_URI: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
