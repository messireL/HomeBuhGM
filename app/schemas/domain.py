from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    username: str
    password: str

class AccountCreate(BaseModel):
    name: str
    initial_balance: float = 0.0

class AccountResponse(BaseModel):
    id: int
    name: str
    # Сумму в ответе пока не шлем, так как она зашифрована
    class Config:
        from_attributes = True