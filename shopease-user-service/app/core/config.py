import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    APP_NAME = os.getenv("APP_NAME", "ShopEase User Management Service")
    DATABASE_URL = os.getenv("DATABASE_URL")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
    AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://localhost:8002")
    PORT = int(os.getenv("PORT", "8004"))

settings = Settings()

if not settings.DATABASE_URL:
    raise RuntimeError("DATABASE_URL is missing")

if not settings.JWT_SECRET_KEY:
    raise RuntimeError("JWT_SECRET_KEY is missing")