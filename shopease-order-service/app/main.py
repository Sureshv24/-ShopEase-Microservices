from fastapi import FastAPI
from app.core.config import settings
from app.routers.order_routes import router
app=FastAPI(title=settings.APP_NAME,version="1.0.0",description="ShopEase Order Management Microservice")
app.include_router(router)
@app.get("/")
def root(): return {"message":"ShopEase Order Management Service","status":"running"}
@app.get("/health")
def health(): return {"status":"healthy"}
