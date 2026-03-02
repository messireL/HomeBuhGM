from decimal import Decimal
from app.services.crypto_service import EncryptionService

class ReportService:
    @staticmethod
    def calculate_balance(transactions: list, private_key: str) -> Decimal:
        total = Decimal("0.00")
        # Создаем сервис с приватным ключом для дешифровки
        crypto = EncryptionService(user_public_key=None, user_private_key=private_key.encode())
        
        for t in transactions:
            amount = crypto.decrypt_amount(t.encrypted_amount)
            if t.type == "income":
                total += amount
            else:
                total -= amount
        return total