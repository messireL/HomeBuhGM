from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database.session import Base
import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String) # SHA-256
    public_key = Column(String)      # Для шифрования данных этого пользователя

class Account(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    encrypted_balance = Column(String) # RSA зашифрованная сумма
    user_id = Column(Integer, ForeignKey("users.id"))
    
    owner = relationship("User", back_populates="accounts")

User.accounts = relationship("Account", back_populates="owner")

from sqlalchemy import Enum
import enum

class TransactionType(enum.Enum):
    INCOME = "income"
    EXPENSE = "expense"
    TRANSFER = "transfer"

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    encrypted_amount = Column(String)  # RSA зашифрованная сумма
    type = Column(String)              # Тип из TransactionType
    category_id = Column(Integer, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id"))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    account = relationship("Account", back_populates="transactions")

Account.transactions = relationship("Transaction", back_populates="account")

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    parent_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    subcategories = relationship("Category")