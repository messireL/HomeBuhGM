from sqlalchemy.orm import Session
from app.models.domain import Account
from app.services.crypto_service import EncryptionService

def create_user_account(db: Session, name: str, initial_balance: float, user_id: int, public_key: bytes):
    crypto = EncryptionService(user_public_key=public_key)
    encrypted_val = crypto.encrypt_amount(initial_balance)
    
    db_account = Account(
        name=name,
        encrypted_balance=encrypted_val,
        user_id=user_id
    )
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account