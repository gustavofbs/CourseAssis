import os
from cryptography.fernet import Fernet
from pathlib import Path
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class DatabaseSecurity:
    def __init__(self, key_file: str = None):
        self.key_file = key_file or os.path.join(os.path.dirname(__file__), 'db.key')
        self._ensure_key_exists()
    
    def _ensure_key_exists(self):
        """Garante que a chave de criptografia existe"""
        if not os.path.exists(self.key_file):
            key = Fernet.generate_key()
            os.makedirs(os.path.dirname(self.key_file), exist_ok=True)
            with open(self.key_file, 'wb') as f:
                f.write(key)
    
    def get_key(self) -> bytes:
        """Recupera a chave de criptografia"""
        with open(self.key_file, 'rb') as f:
            return f.read()
    
    @staticmethod
    def derive_key(password: str, salt: bytes = None) -> tuple:
        """Deriva uma chave a partir de uma senha"""
        if salt is None:
            salt = os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return Fernet(key), salt

    def secure_database_path(self, db_path: str) -> str:
        """Garante que o caminho do banco de dados é seguro"""
        db_dir = os.path.dirname(db_path)
        # Cria o diretório se não existir
        os.makedirs(db_dir, exist_ok=True)
        # Define permissões restritas para o diretório
        os.chmod(db_dir, 0o700)  # Somente o proprietário pode ler/escrever
        return db_path
