import os

class Settings:
    APP_NAME = os.getenv("APP_NAME", "ShopEase Product Service")
    VERSION = "1.0.0"
    PORT = int(os.getenv("PORT", "8003"))

settings = Settings()
