import uuid
from typing import Optional, List
from sqlmodel import SQLModel, Field
from sqlalchemy import ARRAY, Column, String

class LineItemsBase(SQLModel):
    order_id: int = Field(index=True, nullable=True)
    name: str = Field(index=True)
    product_id: int = Field(index=True)
    variation_id: int = Field(default=0)
    quantity: int = Field(default=1)
    tax_class: Optional[str] = Field(default="")
    subtotal: Optional[str] = Field(default="")
    subtotal_tax: Optional[str] = Field(default="")
    total: Optional[str] = Field(default="")
    total_tax: Optional[str] = Field(default="")
    sku: Optional[str] = Field(default="")
    price: int = Field(default=0)
    

class LineItems(LineItemsBase, table=True):
    __tablename__ = "line_items"
    id: int = Field(primary_key=True)
