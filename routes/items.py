from fastapi import APIRouter, Depends, HTTPException, Request
from sqlmodel import Session
from database import get_db
from models import Item
from crud import create_item, get_items, update_stock
from typing import Optional
from datetime import datetime
import os

router = APIRouter()
INVENTORY_SERVICE_URL = os.getenv("INVENTORY_SERVICE_URL")
AUTHENTICATION_SERVICE_URL = os.getenv("AUTHENTICATION_SERVICE_URL")

@router.post("/", response_model=Item)
def create_new_item(item: Item, request: Request, db: Session = Depends(get_db)):
    if request.headers.get('origin') != AUTHENTICATION_SERVICE_URL:
        raise HTTPException(status_code=403, detail="Origin not allowed.")
    item.createdAt = datetime.now()
    item.modifiedAt = datetime.now()
    return create_item(db, item)

@router.get("/", response_model=list[Item])
def read_items(request: Request, category_id: Optional[int] = None, db: Session = Depends(get_db)):
    if request.headers.get('origin') != AUTHENTICATION_SERVICE_URL:
        raise HTTPException(status_code=403, detail="Origin not allowed.")
    return get_items(db, category_id, request.headers.get("email"))

@router.put("/{item_id}/update_stock", response_model=Item)
def modify_stock(request: Request, item_id: int, quantity: int, transaction_type: str, db: Session = Depends(get_db)):
    if request.headers.get('origin') != AUTHENTICATION_SERVICE_URL:
        raise HTTPException(status_code=403, detail="Origin not allowed.")
    try:
        return update_stock(db, item_id, quantity, transaction_type)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
