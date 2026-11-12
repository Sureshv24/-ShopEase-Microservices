from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import update
from app.models.product_model import Product
from app.models.inventory_model import InventoryTransaction
from app.core.config import settings

def stock_change(db: Session, product_id: int, quantity: int, kind: str, remarks=None):
    try:
        product = db.query(Product).filter(Product.id == product_id).with_for_update().first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        previous = product.stock_quantity
        if kind == "OUT" and previous < quantity:
            raise HTTPException(status_code=409, detail="Insufficient stock")
        updated = previous + quantity if kind == "IN" else previous - quantity
        product.stock_quantity = updated
        tx = InventoryTransaction(
            product_id=product_id, transaction_type=kind, quantity=quantity,
            previous_stock=previous, updated_stock=updated, remarks=remarks
        )
        db.add(tx)
        db.commit()
        db.refresh(product)
        db.refresh(tx)
        return product, tx
    except Exception:
        db.rollback()
        raise

def get_stock(db: Session, product_id: int):
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"product_id": product.id, "stock_quantity": product.stock_quantity}

def history(db: Session, product_id: int):
    if not db.get(Product, product_id):
        raise HTTPException(status_code=404, detail="Product not found")
    return db.query(InventoryTransaction).filter(
        InventoryTransaction.product_id == product_id
    ).order_by(InventoryTransaction.created_at.desc()).all()

def low_stock(db: Session, threshold: int | None = None):
    limit = settings.LOW_STOCK_THRESHOLD if threshold is None else threshold
    return db.query(Product).filter(
        Product.is_active.is_(True), Product.stock_quantity <= limit
    ).order_by(Product.stock_quantity.asc()).all()