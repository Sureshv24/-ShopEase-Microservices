from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

@dataclass
class Product:
    product_id: str
    name: str
    description: str | None
    price: float
    stock_quantity: int
    category: str
    status: str
    created_date: datetime
