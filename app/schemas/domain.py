from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Enum
from sqlalchemy.orm import relationship
from app.database.session import Base
import datetime
import enum

class TransactionType(enum.Enum):
    INCOME = "income"
    EXPENSE = "expense"
    TRANSFER = "transfer"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    public_key = Column(String)

    accounts = relationship("Account", back_populates="owner")
    debts = relationship("Debt", back_populates="user")
    categories = relationship("Category", back_populates="user")

class Currency(Base):
    __tablename__ = "currencies"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(3), unique=True, nullable=False) 
    rate_to_base = Column(String) # Храним как строку для точности Decimal

    accounts = relationship("Account", back_populates="currency")

class Account(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    encrypted_balance = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    currency_id = Column(Integer, ForeignKey("currencies.id"))
    
    currency = relationship("Currency", back_populates="accounts")
    owner = relationship("User", back_populates="accounts")
    transactions = relationship("Transaction", back_populates="account")

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    parent_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="categories")
    subcategories = relationship("Category")
    transactions = relationship("Transaction", back_populates="category")

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    encrypted_amount = Column(String)
    type = Column(Enum(TransactionType))
    category_id = Column(Integer, ForeignKey("categories.id"), index=True)
    account_id = Column(Integer, ForeignKey("accounts.id"))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    account = relationship("Account", back_populates="transactions")
    category = relationship("Category", back_populates="transactions")

class Debt(Base):
    __tablename__ = "debts"
    id = Column(Integer, primary_key=True, index=True)
    person_name = Column(String, nullable=False)
    encrypted_amount = Column(String)
    is_my_debt = Column(Boolean, default=True)
    due_date = Column(DateTime, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    user = relationship("User", back_populates="debts")