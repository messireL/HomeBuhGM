import datetime
import enum
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Enum
from sqlalchemy.orm import relationship
from app.database.session import Base

# --- Перечисления ---
class TransactionType(enum.Enum):
    INCOME = "income"
    EXPENSE = "expense"
    TRANSFER = "transfer"

# --- Модели ---

class User(Base):
    """Пользователь системы с RSA ключом для дешифровки своих данных."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)  # SHA-256
    public_key = Column(String, nullable=False)       # RSA Public Key

    # Отношения
    accounts = relationship("Account", back_populates="owner", cascade="all, delete-orphan")
    debts = relationship("Debt", back_populates="user", cascade="all, delete-orphan")
    categories = relationship("Category", back_populates="user", cascade="all, delete-orphan")


class Currency(Base):
    """Справочник валют и их курсов к базовой валюте."""
    __tablename__ = "currencies"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(3), unique=True, nullable=False, index=True) # USD, RUB
    rate_to_base = Column(String, default="1.0") # Курс (строка для Decimal)

    accounts = relationship("Account", back_populates="currency")


class Account(Base):
    """Счета пользователя (карты, наличные, вклады)."""
    __tablename__ = "accounts"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    encrypted_balance = Column(String, nullable=False) # RSA зашифровано
    
    user_id = Column(Integer, ForeignKey("users.id"))
    currency_id = Column(Integer, ForeignKey("currencies.id"))
    
    # Отношения
    owner = relationship("User", back_populates="accounts")
    currency = relationship("Currency", back_populates="accounts")
    transactions = relationship("Transaction", back_populates="account", cascade="all, delete-orphan")


class Category(Base):
    """Категории операций с поддержкой вложенности (Дерево)."""
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    parent_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    # Отношения
    user = relationship("User", back_populates="categories")
    # Исправленная логика иерархии
    parent = relationship("Category", remote_side=[id], back_populates="subcategories")
    subcategories = relationship("Category", back_populates="parent", cascade="all, delete-orphan")
    transactions = relationship("Transaction", back_populates="category")



class Transaction(Base):
    """Движение денежных средств."""
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    encrypted_amount = Column(String, nullable=False) # RSA зашифровано
    # Добавлено имя для Enum, чтобы PostgreSQL не выдавал ошибку
    type = Column(Enum(TransactionType, name="transaction_type_enum"), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    account_id = Column(Integer, ForeignKey("accounts.id"))
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    
    # Отношения
    account = relationship("Account", back_populates="transactions")
    category = relationship("Category", back_populates="transactions")


class Debt(Base):
    """Учет долгов и кредитов."""
    __tablename__ = "debts"
    
    id = Column(Integer, primary_key=True, index=True)
    person_name = Column(String, nullable=False)
    encrypted_amount = Column(String, nullable=False) # RSA зашифровано
    is_my_debt = Column(Boolean, default=True)      # True - я должен, False - мне должны
    due_date = Column(DateTime, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    user = relationship("User", back_populates="debts")