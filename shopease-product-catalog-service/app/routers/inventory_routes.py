from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.core.security import require_admin
from app.schemas.inventory_schema import StockChange, InventoryResponse, InventoryTransactionResponse
from app.schemas.product_schema import ProductResponse
from app.services import inventory_service

router = APIRouter(prefix="/api/inventory", tags=["Inventory"])

@router.get("/low-stock", response_model=list[ProductResponse])
def low_stock(threshold: int | None = Query(default=None, ge=0), db: Session = Depends(get_db), admin=Depends(require_admin)):
    return inventory_service.low_stock(db, threshold)

@router.get("/{product_id}", response_model=InventoryResponse)
def get_stock(product_id: int, db: Session = Depends(get_db)):
    return inventory_service.get_stock(db, product_id)

@router.post("/{product_id}/stock-in", response_model=InventoryResponse)
def stock_in(product_id: int, data: StockChange, db: Session = Depends(get_db), admin=Depends(require_admin)):
    product, _ = inventory_service.stock_change(db, product_id, data.quantity, "IN", data.remarks)
    return {"product_id": product.id, "stock_quantity": product.stock_quantity}

@router.post("/{product_id}/stock-out", response_model=InventoryResponse)
def stock_out(product_id: int, data: StockChange, db: Session = Depends(get_db), admin=Depends(require_admin)):
    product, _ = inventory_service.stock_change(db, product_id, data.quantity, "OUT", data.remarks)
    return {"product_id": product.id, "stock_quantity": product.stock_quantity}

@router.get("/{product_id}/history", response_model=list[InventoryTransactionResponse])
def get_history(product_id: int, db: Session = Depends(get_db), admin=Depends(require_admin)):
    return inventory_service.history(db, product_id)