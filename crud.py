from sqlmodel import Session, select
from models import Item, Category, Transaction
from typing import Optional
import os
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TRANSACTION_SERVICE_URL = os.getenv("TRANSACTION_SERVICE_URL")
INVENTORY_SERVICE_URL = os.getenv("INVENTORY_SERVICE_URL")

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

def get_item_by_id(db:Session, id:str) -> Item:
    query = select(Item).where(Item.id == id)
    return db.exec(query).first()

def update_stock(db: Session, item_id: int, quantity: int, transaction_type: str):
    print("id nya berapa", item_id)
    item = get_item_by_id(db, item_id)
    print("item: ", item)
    if not item:
        raise ValueError("Item not found")
    
    print('kalo sini')
    
    # Update stock based on transaction type
    if transaction_type == "in":
        item.stock += quantity
    elif transaction_type == "out":
        if item.stock < quantity:
            raise ValueError("Insufficient stock")
        item.stock -= quantity
    else:
        raise ValueError("Invalid transaction type")

    item.modifiedAt = datetime.now()

    print('tembus sini ga')

    # Commit stock update to the database
    db.add(item)
    db.commit()
    db.refresh(item)

    # Post transaction to transaction microservice
    post_transaction_to_service(item_id, item.account_email, quantity, transaction_type)

    return item

def post_transaction_to_service(item_id: int, account_email:str, quantity: int, transaction_type: str):
    transaction_data:Transaction = {
        'account_email': account_email,
        'item_id': item_id,
        'transaction_type': transaction_type,
        'quantity': quantity,
    }
    # print('payload: ',transaction_data)

    # print('sampai sini kan')
    # print(TRANSACTION_SERVICE_URL)
    # print(INVENTORY_URL)

    try:
        response = requests.post(f"{TRANSACTION_SERVICE_URL}/api/transactions", json=transaction_data, headers={"origin":INVENTORY_SERVICE_URL})
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
