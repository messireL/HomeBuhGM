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

class Currency(Base):
    __tablename__ = "currencies"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(3), unique=True, nullable=False) # USD, EUR, RUB
    rate_to_base = Column(String) # Зашифрованный или открытый коэффициент (лучше открытый для аналитики)
    
    accounts = relationship("Account", back_populates="currency")

# Обновите Account:
class Account(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    encrypted_balance = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    currency_id = Column(Integer, ForeignKey("currencies.id")) # Ссылка на валюту
    
    currency = relationship("Currency", back_populates="accounts")
    owner = relationship("User", back_populates="accounts")
    transactions = relationship("Transaction", back_populates="account")