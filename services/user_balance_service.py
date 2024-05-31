from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.user_balance import UserBalance
from repositories.user_balance_repository import UserBalanceRepository


class UserBalanceService:
    def __init__(self, session: Session):
        self.repository = UserBalanceRepository(session)

    def add_balance(self, user_id: UUID, amount: int) -> UserBalance:
        return self.repository.update_balance(user_id, amount)
    
    def get_balance(self, user_id: UUID):
        user_balance = self.repository.get_by_user_id(user_id)
        if not user_balance:
            raise HTTPException(status_code=404, detail="User balance not found")
        return user_balance
