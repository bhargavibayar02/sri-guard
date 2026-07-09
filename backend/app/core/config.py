# config.py
# This file reads our secret settings from the .env file
# so we never hard-code passwords or keys directly in our code.

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # MongoDB connection string (local or Atlas)
    MONGO_URI: str = "mongodb://localhost:27017"

    # Name of the database inside MongoDB
    DB_NAME: str = "sriguard"

    # Secret key used to sign JWT tokens (keep this private!)
    JWT_SECRET: str = "change_this_secret"

    # Algorithm used to sign JWT tokens
    JWT_ALGORITHM: str = "HS256"

    # How long a login session (token) stays valid, in minutes
    JWT_EXPIRE_MINUTES: int = 60

    class Config:
        env_file = ".env"  # tells pydantic to load values from .env

# Create one shared settings object that the whole app can import
settings = Settings()