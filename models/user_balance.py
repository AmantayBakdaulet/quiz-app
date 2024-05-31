import uuid

from sqlalchemy import Column, Integer, UUID

from dependencies.database import Base


class UserBalance(Base):
    __tablename__ = "user_balances"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    balance = Column(Integer, default=0)
