import hashlib
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64

class CryptoManager:
    @staticmethod
    def hash_password(password: str) -> str:
        """SHA-256 хеширование пароля."""
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def generate_rsa_keys():
        """Генерация пары ключей RSA."""
        key = RSA.generate(2048)
        private_key = key.export_key()
        public_key = key.publickey().export_key()
        return private_key, public_key

    @staticmethod
    def encrypt_data(data: str, public_key_str: bytes) -> str:
        """Шифрование данных RSA."""
        recipient_key = RSA.import_key(public_key_str)
        cipher_rsa = PKCS1_OAEP.new(recipient_key)
        enc_data = cipher_rsa.encrypt(data.encode())
        return base64.b64encode(enc_data).decode()