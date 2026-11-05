from fastapi import FastAPI
from app.core.config import settings
from app.routers.auth_routes import router as auth_router

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="Independent ShopEase Authentication Microservice"
)

app.include_router(auth_router)

@app.get("/")
def root():
    return {
        "message": "ShopEase Authentication Service",
        "status": "running"
    }

@app.get("/health")
def health():
    return {"status": "healthy"}
