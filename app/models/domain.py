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