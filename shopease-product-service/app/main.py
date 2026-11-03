from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.routers.product_routes import router as product_router
from app.config.settings import settings

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="ShopEase Product Microservice API"
)

app.include_router(product_router)

@app.get("/")
def root():
    return {"message": "Welcome to ShopEase Product Service", "status": "running"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.exception_handler(Exception)
async def unexpected_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )
