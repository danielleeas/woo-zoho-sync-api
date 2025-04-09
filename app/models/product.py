import uuid
from typing import Optional, List
from sqlmodel import SQLModel, Field
from sqlalchemy import ARRAY, Column, String

class ProductBase(SQLModel):
    parent_id: int = Field(index=True, nullable=True)
    product_id: int = Field(index=True, nullable=True)
    name: Optional[str] = Field(index=True)
    slug: Optional[str] = Field(max_length=255)
    permalink: Optional[str] = Field(max_length=255, unique=True)
    date_created: Optional[str] = Field(default=None)
    date_modified: Optional[str] = Field(default=None)
    type: Optional[str] = Field(max_length=20, default="simple")
    status: Optional[str] = Field(max_length=20, default="publish")
    featured: Optional[bool] = Field(default=False)
    description: Optional[str] = Field(default="")
    sku: Optional[str] = Field(max_length=100)
    price: Optional[str] = Field(default="")
    purchase_price: Optional[str] = Field(default="")
    regular_price: Optional[str] = Field(default="")
    stock_quantity: int = Field(ge=0)
    weight: Optional[str] = Field(default="")
    length: Optional[str] = Field(default="")
    width: Optional[str] = Field(default="")
    height: Optional[str] = Field(default="")
    categories: List[str] = Field(sa_column=Column(ARRAY(String)), default=[])
    images: List[str] = Field(sa_column=Column(ARRAY(String)), default=[])
    attribute_name: Optional[str] = Field(default="")
    attribute_value: Optional[str] = Field(default="")

class Product(ProductBase, table=True):
    __tablename__ = "products"
    id: int = Field(primary_key=True)
