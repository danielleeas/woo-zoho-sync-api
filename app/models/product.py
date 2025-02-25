import uuid
from typing import Optional, List
from sqlmodel import SQLModel, Field
from sqlalchemy import ARRAY, Column, String

class ProductBase(SQLModel):
    parent_id: int = Field(index=True, nullable=True)
    name: str = Field(index=True)
    slug: str = Field(max_length=255)
    permalink: str = Field(max_length=255, unique=True)
    date_created: str = Field(index=True)
    date_modified: str = Field(max_length=50)
    type: str = Field(max_length=20, default="simple")
    status: str = Field(max_length=20, default="publish")
    featured: bool = Field(default=False)
    description: str = Field(default="")
    sku: str = Field(max_length=100)
    price: str = Field(default="")
    purchase_price: str = Field(default="")
    regular_price: str = Field(default="")
    stock_quantity: int = Field(ge=0)
    weight: Optional[str] = Field(default="")
    length: Optional[str] = Field(default="")
    width: Optional[str] = Field(default="")
    height: Optional[str] = Field(default="")
    categories: List[str] = Field(sa_column=Column(ARRAY(String)), default=[])
    images: List[str] = Field(sa_column=Column(ARRAY(String)), default=[])
    attribute_name: str = Field(default="")
    attribute_value: str = Field(default="")

class Product(ProductBase, table=True):
    __tablename__ = "products"
    id: int = Field(primary_key=True)
