from fastapi import FastAPI
from app.core.config import settings
from app.routers.product_routes import router as product_router
from app.routers.category_routes import router as category_router
from app.routers.inventory_routes import router as inventory_router

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="Independent ShopEase product catalog, category and inventory microservice"
)
app.include_router(product_router)
app.include_router(category_router)
app.include_router(inventory_router)

@app.get("/")
def root():
    return {"message": "ShopEase Product Catalog Service", "status": "running"}

@app.get("/health")
def health():
    return {"status": "healthy"}