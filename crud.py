from sqlmodel import Session, select
from models import Item, Category, Transaction
from typing import Optional

# CRUD for Item
def create_item(db: Session, item: Item):
    db.add(item)
    db.commit()
    db.refresh(item)
    # Automatically log a transaction for the stock added
    if item.stock > 0:
        create_transaction(db, Transaction(item_id=item.id, quantity=item.stock, transaction_type="in"))
    return item

def get_items(db: Session, category_id: Optional[int] = None):
    query = select(Item)
    if category_id:
        query = query.where(Item.category_id == category_id)
    return db.exec(query).all()

def update_stock(db: Session, item_id: int, quantity: int, transaction_type: str):
    item = db.get(Item, item_id)
    if not item:
        raise ValueError("Item not found")
    if transaction_type == "in":
        item.stock += quantity
    elif transaction_type == "out":
        if item.stock < quantity:
            raise ValueError("Insufficient stock")
        item.stock -= quantity
    else:
        raise ValueError("Invalid transaction type")
    db.add(item)
    db.commit()
    db.refresh(item)
    # Log the transaction
    create_transaction(db, Transaction(item_id=item.id, quantity=quantity, transaction_type=transaction_type))
    return item

# CRUD for Category
def create_category(db: Session, category: Category):
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

def get_categories(db: Session):
    return db.exec(select(Category)).all()

# CRUD for Transaction
def create_transaction(db: Session, transaction: Transaction):
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction

def get_transactions(db: Session):
    return db.exec(select(Transaction)).all()
