from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Session

from models.user_balance import UserBalance


class UserBalanceRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_user_id(self, user_id: UUID) -> UserBalance:
        return self.session.query(UserBalance).filter(UserBalance.user_id == user_id).first()

    def create(self, user_id: UUID) -> UserBalance:
        user_balance = UserBalance(user_id=user_id)
        self.session.add(user_balance)
        self.session.commit()
        self.session.refresh(user_balance)
        return user_balance

    def update_balance(self, user_id: UUID, amount: int) -> UserBalance:
        user_balance = self.get_by_user_id(user_id)
        if not user_balance:
            user_balance = self.create(user_id)
        user_balance.balance += amount
        self.session.commit()
        self.session.refresh(user_balance)
        return user_balance
