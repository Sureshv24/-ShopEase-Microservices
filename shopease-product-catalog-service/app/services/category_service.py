from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.category_model import Category
from app.models.product_model import Product

def create_category(db: Session, data: dict):
    obj = Category(**data)
    db.add(obj)
    try:
        db.commit()
        db.refresh(obj)
        return obj
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Category name already exists")

def list_categories(db: Session):
    return db.query(Category).filter(Category.is_active.is_(True)).order_by(Category.name).all()

def get_category(db: Session, category_id: int):
    obj = db.get(Category, category_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Category not found")
    return obj

def update_category(db: Session, category_id: int, data: dict):
    obj = get_category(db, category_id)
    for k, v in data.items():
        setattr(obj, k, v)
    try:
        db.commit()
        db.refresh(obj)
        return obj
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Category name already exists")

def delete_category(db: Session, category_id: int):
    obj = get_category(db, category_id)
    if db.query(Product).filter(Product.category_id == category_id).first():
        raise HTTPException(status_code=409, detail="Category contains products; reassign or remove products first")
    db.delete(obj)
    db.commit()