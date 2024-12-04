from fastapi import APIRouter, Depends
from sqlmodel import Session
from database import get_db
from models import Transaction
from crud import get_transactions

router = APIRouter()

@router.get("/", response_model=list[Transaction])
def read_transactions(db: Session = Depends(get_db)):
    return get_transactions(db)
