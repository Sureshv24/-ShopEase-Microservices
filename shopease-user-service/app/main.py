from fastapi import FastAPI
from app.core.config import settings
from app.routers.user_routes import router as user_router
from app.routers.address_routes import router as address_router

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="ShopEase User Management Microservice"
)

app.include_router(user_router)
app.include_router(address_router)

@app.get("/")
def root():
    return {"message": "ShopEase User Management Service", "status": "running"}

@app.get("/health")
def health():
    return {"status": "healthy"}