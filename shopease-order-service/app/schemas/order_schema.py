from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field
from typing import Literal
class OrderItemInput(BaseModel):
    product_id: int = Field(gt=0)
    quantity: int = Field(gt=0, le=1000)
class OrderCreate(BaseModel):
    items: list[OrderItemInput] = Field(min_length=1, max_length=50)
    shipping_address_id: int = Field(gt=0)
    notes: str | None = Field(default=None, max_length=1000)
class StatusUpdate(BaseModel):
    order_status: Literal["CONFIRMED","PROCESSING","SHIPPED","DELIVERED","CANCELLED"]
class ItemOutput(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    product_id: int
    product_name: str
    sku: str
    unit_price: Decimal
    quantity: int
    discount_amount: Decimal
    total_price: Decimal
    created_at: datetime
class OrderOutput(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    order_number: str
    user_id: int
    shipping_address: dict
    subtotal: Decimal
    discount_amount: Decimal
    shipping_charge: Decimal
    tax_amount: Decimal
    total_amount: Decimal
    order_status: str
    payment_status: str
    notes: str | None
    created_at: datetime
    updated_at: datetime
    items: list[ItemOutput] = []
class OrderPage(BaseModel):
    total: int
    page: int
    page_size: int
    items: list[OrderOutput]
