from fastapi import APIRouter, Depends, Request, HTTPException
from sqlmodel import Session
from database import get_db
from models import Category
from crud import create_category, get_categories
from datetime import datetime
import os

router = APIRouter()
INVENTORY_SERVICE_URL = os.getenv("INVENTORY_SERVICE_URL")
AUTHENTICATION_SERVICE_URL = os.getenv("AUTHENTICATION_SERVICE_URL")

@router.post("/", response_model=Category)
def create_new_category(request: Request, category: Category, db: Session = Depends(get_db)):
    if request.headers.get('origin') != AUTHENTICATION_SERVICE_URL:
        raise HTTPException(status_code=403, detail="Origin not allowed.")
    category.createdAt = datetime.now()
    category.modifiedAt = datetime.now()
    return create_category(db, category)

@router.get("/", response_model=list[Category])
def read_categories(request: Request, db: Session = Depends(get_db)):
    if request.headers.get('origin') != AUTHENTICATION_SERVICE_URL:
        raise HTTPException(status_code=403, detail="Origin not allowed.")
    return get_categories(db)
