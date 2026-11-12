from decimal import Decimal
from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.core.security import current_user, require_admin
from app.schemas.product_schema import ProductCreate, ProductUpdate, ProductResponse
from app.services import product_service

router = APIRouter(prefix="/api/products", tags=["Products"])

@router.post("/", response_model=ProductResponse, status_code=201)
def create(data: ProductCreate, db: Session = Depends(get_db), admin=Depends(require_admin)):
    return product_service.create_product(db, data.model_dump())

@router.get("/", response_model=list[ProductResponse])
def list_all(
    search: str | None = None,
    category_id: int | None = Query(default=None, gt=0),
    min_price: Decimal | None = Query(default=None, ge=0),
    max_price: Decimal | None = Query(default=None, ge=0),
    available: bool | None = None,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    sort_by: str = Query(default="created_at", pattern="^(name|price|created_at)$"),
    sort_order: str = Query(default="desc", pattern="^(asc|desc)$"),
    db: Session = Depends(get_db)
):
    if min_price is not None and max_price is not None and min_price > max_price:
        from fastapi import HTTPException
        raise HTTPException(status_code=422, detail="min_price cannot exceed max_price")
    return product_service.list_products(
        db, search=search, category_id=category_id, min_price=min_price,
        max_price=max_price, available=available, page=page, page_size=page_size,
        sort_by=sort_by, sort_order=sort_order
    )

@router.get("/{product_id}", response_model=ProductResponse)
def get_one(product_id: int, db: Session = Depends(get_db)):
    product = product_service.get_product(db, product_id)
    if not product.is_active:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/{product_id}", response_model=ProductResponse)
def replace(product_id: int, data: ProductCreate, db: Session = Depends(get_db), admin=Depends(require_admin)):
    return product_service.update_product(db, product_id, data.model_dump())

@router.patch("/{product_id}", response_model=ProductResponse)
def patch(product_id: int, data: ProductUpdate, db: Session = Depends(get_db), admin=Depends(require_admin)):
    return product_service.update_product(db, product_id, data.model_dump(exclude_unset=True))

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(product_id: int, db: Session = Depends(get_db), admin=Depends(require_admin)):
    product_service.delete_product(db, product_id)
    return Response(status_code=204)