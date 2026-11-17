import os
from decimal import Decimal
from dotenv import load_dotenv
load_dotenv()
class Settings:
    APP_NAME = os.getenv("APP_NAME", "ShopEase Order Management Service")
    DATABASE_URL = os.getenv("DATABASE_URL")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
    USER_SERVICE_URL = os.getenv("USER_SERVICE_URL", "http://host.docker.internal:8004")
    PRODUCT_SERVICE_URL = os.getenv("PRODUCT_SERVICE_URL", "http://host.docker.internal:8005")
    INVENTORY_SERVICE_TOKEN = os.getenv("INVENTORY_SERVICE_TOKEN", "")
    HTTP_TIMEOUT = float(os.getenv("HTTP_TIMEOUT", "8"))
    TAX_RATE = Decimal(os.getenv("TAX_RATE", "0.05"))
    SHIPPING_CHARGE = Decimal(os.getenv("SHIPPING_CHARGE", "50.00"))
    FREE_SHIPPING_THRESHOLD = Decimal(os.getenv("FREE_SHIPPING_THRESHOLD", "1000.00"))
settings = Settings()
if not settings.DATABASE_URL or not settings.JWT_SECRET_KEY:
    raise RuntimeError("DATABASE_URL and JWT_SECRET_KEY must be configured")
