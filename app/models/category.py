import uuid
from sqlmodel import SQLModel, Field

class CategoryBase(SQLModel):
    name: str
    slug: str

class Category(CategoryBase, table=True):
    __tablename__ = "categories"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
