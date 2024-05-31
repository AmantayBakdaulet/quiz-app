from uuid import UUID

from pydantic import BaseModel


class UserBalanceResponse(BaseModel):
    user_id: UUID
    balance: int

    class Config:
        orm_mode = True
