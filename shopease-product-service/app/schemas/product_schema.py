from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, ConfigDict, field_validator

class ProductStatus(str, Enum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"

class ProductCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    price: float = Field(gt=0)
    stock_quantity: int = Field(ge=0)
    category: str = Field(min_length=2, max_length=50)
    status: ProductStatus = ProductStatus.ACTIVE

    @field_validator("name", "category")
    @classmethod
    def validate_text(cls, value):
        value = value.strip()
        if not value:
            raise ValueError("This field cannot be empty")
        return value

class ProductUpdate(ProductCreate):
    pass

class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    product_id: str
    name: str
    description: str | None
    price: float
    stock_quantity: int
    category: str
    status: ProductStatus
    created_date: datetime
