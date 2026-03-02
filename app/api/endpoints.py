from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from app.database.session import SessionLocal
from app.models.domain import User, Account, Debt
from app.services.crypto_service import EncryptionService
from app.core.security import CryptoManager

router = APIRouter()

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

# --- Schemas ---
class DebtCreate(BaseModel):
    person_name: str
    amount: float
    is_my_debt: bool = True
    due_date: Optional[datetime] = None
    user_id: int

# --- Endpoints ---
@router.post("/debts/", status_code=201)
def add_debt(debt_data: DebtCreate, db: Session = Depends(get_db)):
    # 1. Проверка пользователя
    user = db.query(User).filter(User.id == debt_data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # 2. Шифрование суммы
    try:
        crypto = EncryptionService(user_public_key=user.public_key.encode())
        enc_amount = crypto.encrypt_amount(debt_data.amount)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Encryption error: {str(e)}")
    
    # 3. Сохранение в БД
    new_debt = Debt(
        person_name=debt_data.person_name,
        encrypted_amount=enc_amount,
        is_my_debt=debt_data.is_my_debt,
        due_date=debt_data.due_date,
        user_id=debt_data.user_id
    )
    
    db.add(new_debt)
    db.commit()
    db.refresh(new_debt)
    
    return {"status": "success", "debt_id": new_debt.id}