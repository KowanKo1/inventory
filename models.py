from typing import Optional
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime

class AuthCredentials:
    method:str
    token:str

class MetadataBase(SQLModel):
    createdAt: datetime
    modifiedAt: datetime

class AccountBase(MetadataBase):
    password: str
    firstname: str
    lastname: str

class Account(AccountBase, table=True):
    email: str = Field(sa_column_kwargs={"unique":True}, primary_key=True)

# Item Model
class ItemBase(MetadataBase):
    name: str
    code: str
    description: Optional[str] = None
    stock: int = 0
    account_email: str = Field(foreign_key="account.email")
    category_id: int | None = Field(default=None, foreign_key="category.id")

class Item(ItemBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

# Category Model
class CategoryBase(MetadataBase):
    name: str

class Category(CategoryBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

# Transaction Model
class TransactionBase(MetadataBase):
    quantity: int
    transaction_type: str  # "in" or "out"
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    account_email: str = Field( foreign_key="account.email")
    item_id: int = Field( foreign_key="item.id")

class Transaction(TransactionBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
