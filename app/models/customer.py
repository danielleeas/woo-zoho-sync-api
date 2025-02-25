from typing import Optional, List
from sqlmodel import SQLModel, Field

class CustomerBase(SQLModel):
    woo_id: int
    first_name: Optional[str] = Field(default="")
    last_name: Optional[str] = Field(default="")
    username: Optional[str] = Field(default="")
    email: Optional[str] = Field(default="")
    billing_first_name: Optional[str] = Field(default="")
    billing_last_name: Optional[str] = Field(default="")
    billing_company: Optional[str] = Field(default="")
    billing_address_1: Optional[str] = Field(default="")
    billing_address_2: Optional[str] = Field(default="")
    billing_city: Optional[str] = Field(default="")
    billing_postcode: Optional[str] = Field(default="")
    billing_country: Optional[str] = Field(default="")
    billing_state: Optional[str] = Field(default="")
    billing_email: Optional[str] = Field(default="")
    billing_phone: Optional[str] = Field(default="")
    shipping_first_name: Optional[str] = Field(default="")
    shipping_last_name: Optional[str] = Field(default="")
    shipping_company: Optional[str] = Field(default="")
    shipping_address_1: Optional[str] = Field(default="")
    shipping_address_2: Optional[str] = Field(default="")
    shipping_city: Optional[str] = Field(default="")
    shipping_postcode: Optional[str] = Field(default="")
    shipping_country: Optional[str] = Field(default="")
    shipping_state: Optional[str] = Field(default="")
    shipping_phone: Optional[str] = Field(default="")
    is_paying_customer: Optional[bool] = Field(default=False)
    avatar_url: Optional[str] = Field(default="")
    created_at: Optional[str] = Field(default="")
    updated_at: Optional[str] = Field(default="")

class Customer(CustomerBase, table=True):
    __tablename__ = "customers"
    id: int = Field(primary_key=True)
