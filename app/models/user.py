from sqlmodel import SQLModel, Field

class UserBase(SQLModel):
    username: str = Field(max_length=255)
    email: str = Field(max_length=255)
    is_superuser: bool = Field(default=False)
    is_active: bool = Field(default=True)

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: str | None = None

class UserPublic(UserBase):
    id: int

class UserLogin(SQLModel):
    email: str
    password: str

class User(UserBase, table=True):
    __tablename__ = "users"
    id: int = Field(default=None, primary_key=True)
    password: str = Field(max_length=255)