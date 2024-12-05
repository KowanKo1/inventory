from sqlmodel import Session, select
from models import Item, Category
from typing import Optional
import os
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TRANSACTION_SERVICE_URL = os.getenv("TRANSACTION_SERVICE_URL")
INVENTORY_URL = os.getenv("INVENTORY_URL")

# CRUD for Item
def create_item(db: Session, item: Item):
    db.add(item)
    db.commit()
    db.refresh(item)

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
    
    # Update stock based on transaction type
    if transaction_type == "in":
        item.stock += quantity
    elif transaction_type == "out":
        if item.stock < quantity:
            raise ValueError("Insufficient stock")
        item.stock -= quantity
    else:
        raise ValueError("Invalid transaction type")

    # Commit stock update to the database
    db.add(item)
    db.commit()
    db.refresh(item)

    # Post transaction to transaction microservice
    post_transaction_to_service(item_id, quantity, transaction_type)

    return item

def post_transaction_to_service(item_id: int, quantity: int, transaction_type: str):
    transaction_data = {
        "item_id": item_id,
        "quantity": quantity,
        "transaction_type": transaction_type,
        "timestamp": datetime.utcnow().isoformat()
    }
    try:
        response = requests.post(f"{TRANSACTION_SERVICE_URL}/api/transactions", json=transaction_data, headers={"origin":INVENTORY_URL})
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to log transaction: {e}")

# CRUD for Category
def create_category(db: Session, category: Category):
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

def get_categories(db: Session):
    return db.exec(select(Category)).all()
