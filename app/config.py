import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback_secret_key")  # Uses .env, falls back if missing
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///cmdb.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TIMEZONE = 'America/Chicago'