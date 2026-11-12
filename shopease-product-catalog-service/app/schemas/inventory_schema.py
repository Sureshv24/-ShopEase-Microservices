from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

class StockChange(BaseModel):
    quantity: int = Field(gt=0)
    remarks: str | None = Field(default=None, max_length=255)

class InventoryResponse(BaseModel):
    product_id: int
    stock_quantity: int

class InventoryTransactionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    product_id: int
    transaction_type: str
    quantity: int
    previous_stock: int
    updated_stock: int
    remarks: str | None
    created_at: datetime