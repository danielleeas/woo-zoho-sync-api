import uuid
from typing import Optional
from sqlmodel import SQLModel, Field

class ProductBase(SQLModel):
    group_id: str = Field(index=True)
    name: str = Field(max_length=255)
    sku: str = Field(max_length=100, unique=True)
    category_id: str = Field(index=True)
    product_type: str = Field(max_length=50)
    unit: str = Field(max_length=20)
    status: str = Field(max_length=20, default="active")
    description: Optional[str] = Field(default=None)
    brand: Optional[str] = Field(default=None, max_length=100)
    manufacturer: Optional[str] = Field(default=None, max_length=100)
    rate: float = Field(ge=0)
    purchase_rate: float = Field(ge=0)
    tax_id: Optional[str] = Field(default=None)
    initial_stock: float = Field(default=0, ge=0)
    stock_on_hand: float = Field(default=0, ge=0)
    available_stock: float = Field(default=0, ge=0)
    actual_available_stock: float = Field(default=0, ge=0)    
    length: Optional[str] = Field(default=None, max_length=20)
    width: Optional[str] = Field(default=None, max_length=20)
    height: Optional[str] = Field(default=None, max_length=20)
    weight: Optional[str] = Field(default=None, max_length=20)
    weight_unit: Optional[str] = Field(default=None, max_length=10)
    dimension_unit: Optional[str] = Field(default=None, max_length=10)

class Product(ProductBase, table=True):
    __tablename__ = "products"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
