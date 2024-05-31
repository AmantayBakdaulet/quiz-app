import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from dependencies.database import get_db
from schemas.user_balance import UserBalanceResponse
from services.user_balance_service import UserBalanceService


router = APIRouter()

@router.get("/balance/{user_id}", response_model=UserBalanceResponse)
def get_balance(user_id: uuid.UUID, session: Session = Depends(get_db)):
    _service = UserBalanceService(session)
    return _service.get_balance(user_id)

@router.post("/balance/add", response_model=UserBalanceResponse)
def add_balance(user_id: uuid.UUID, amount: int, session: Session = Depends(get_db)):
    _service = UserBalanceService(session)
    return _service.add_balance(user_id, amount)
