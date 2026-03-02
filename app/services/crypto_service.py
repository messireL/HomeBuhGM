from app.core.security import CryptoManager
from decimal import Decimal

class EncryptionService:
    def __init__(self, user_public_key: bytes, user_private_key: bytes = None):
        self.public_key = user_public_key
        self.private_key = user_private_key
        self.crypto = CryptoManager()

    def encrypt_amount(self, amount: Decimal) -> str:
        """Превращает число в зашифрованную строку для БД."""
        return self.crypto.encrypt_data(str(amount), self.public_key)

    def decrypt_amount(self, encrypted_str: str) -> Decimal:
        """Расшифровывает строку из БД обратно в Decimal."""
        if not self.private_key:
            raise ValueError("Приватный ключ не предоставлен")
        # Логика дешифровки (будет добавлена в CryptoManager в этом шаге)
        decrypted_data = self.crypto.decrypt_data(encrypted_str, self.private_key)
        return Decimal(decrypted_data)