import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    APP_NAME = os.getenv("APP_NAME", "ShopEase Authentication Service")
    DATABASE_URL = os.getenv("DATABASE_URL")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
    )

settings = Settings()

if not settings.DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not configured")

if not settings.JWT_SECRET_KEY:
    raise RuntimeError("JWT_SECRET_KEY is not configured")
