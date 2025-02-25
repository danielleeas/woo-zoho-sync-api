import uuid
from typing import Optional
from sqlmodel import SQLModel, Field

class GroupBase(SQLModel):
    group_name: str = Field(max_length=255)
    brand: Optional[str] = Field(default=None)
    manufacturer: Optional[str] = Field(default=None)
    unit: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    tax_id: Optional[str] = Field(default=None)
    attribute_name: Optional[str] = Field(default=None)

class Group(GroupBase, table=True):
    __tablename__ = "groups"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
