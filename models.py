from typing import Optional
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime

# Item Model
class ItemBase(SQLModel):
    name: str
    code: str
    description: Optional[str] = None
    stock: int = 0
    category_id: int

class Item(ItemBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

# Category Model
class CategoryBase(SQLModel):
    name: str

class Category(CategoryBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

# Transaction Model
class TransactionBase(SQLModel):
    item_id: int
    quantity: int
    transaction_type: str  # "in" or "out"
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class Transaction(TransactionBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
