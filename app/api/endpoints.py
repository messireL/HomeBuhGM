from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.schemas.domain import UserCreate, AccountCreate
from app.models.domain import User, Account
from app.core.security import CryptoManager
from app.services.account_service import create_user_account

router = APIRouter()

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

@router.post("/users/")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # 1. SHA-256 для пароля
    hashed = CryptoManager.hash_password(user.password)
    # 2. RSA ключи
    priv, pub = CryptoManager.generate_rsa_keys()
    
    db_user = User(username=user.username, hashed_password=hashed, public_key=pub.decode())
    db.add(db_user)
    db.commit()
    # ВАЖНО: Приватный ключ 'priv' нужно отдать пользователю ОДИН РАЗ (он не хранится в БД)
    return {"status": "created", "private_key": priv.decode()}

@router.post("/accounts/{user_id}")
def add_account(user_id: int, acc: AccountCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user: raise HTTPException(404, "User not found")
    
    new_acc = create_user_account(db, acc.name, acc.initial_balance, user_id, user.public_key.encode())
    return {"id": new_acc.id, "name": new_acc.name}