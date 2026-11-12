from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError
from app.models.product_model import Product
from app.models.category_model import Category

def get_product(db: Session, product_id: int):
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

def create_product(db: Session, data: dict):
    category = db.get(Category, data["category_id"])
    if not category or not category.is_active:
        raise HTTPException(status_code=400, detail="Active category does not exist")
    product = Product(**data)
    db.add(product)
    try:
        db.commit()
        db.refresh(product)
        return product
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="SKU already exists or product data conflicts")

def list_products(db: Session, *, search=None, category_id=None, min_price=None,
                  max_price=None, available=None, page=1, page_size=10,
                  sort_by="created_at", sort_order="desc", include_inactive=False):
    q = db.query(Product)
    if not include_inactive:
        q = q.filter(Product.is_active.is_(True))
    if search:
        term = f"%{search.strip()}%"
        q = q.filter(or_(Product.name.ilike(term), Product.sku.ilike(term)))
    if category_id is not None:
        q = q.filter(Product.category_id == category_id)
    if min_price is not None:
        q = q.filter(Product.price >= min_price)
    if max_price is not None:
        q = q.filter(Product.price <= max_price)
    if available is True:
        q = q.filter(Product.stock_quantity > 0)
    elif available is False:
        q = q.filter(Product.stock_quantity == 0)
    allowed = {"name": Product.name, "price": Product.price, "created_at": Product.created_at}
    column = allowed.get(sort_by, Product.created_at)
    q = q.order_by(column.asc() if sort_order == "asc" else column.desc())
    return q.offset((page - 1) * page_size).limit(page_size).all()

def update_product(db: Session, product_id: int, data: dict):
    product = get_product(db, product_id)
    if "category_id" in data:
        category = db.get(Category, data["category_id"])
        if not category or not category.is_active:
            raise HTTPException(status_code=400, detail="Active category does not exist")
    for k, v in data.items():
        setattr(product, k, v)
    if product.discount_price is not None and product.discount_price > product.price:
        raise HTTPException(status_code=400, detail="discount_price cannot exceed price")
    try:
        db.commit()
        db.refresh(product)
        return product
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="SKU already exists")

def delete_product(db: Session, product_id: int):
    product = get_product(db, product_id)
    db.delete(product)
    db.commit()