from abc import ABC, abstractmethod
import sqlite3
from typing import Dict, List

class DataStorage(ABC):
    """Classe abstrata base para armazenamento de dados"""
    
    @abstractmethod
    def save_user(self, user_data: Dict) -> int:
        """Salva dados do usuário e retorna o ID"""
        pass
    
    @abstractmethod
    def save_recommendation(self, user_id: int, recommendation_data: Dict) -> int:
        """Salva uma recomendação para um usuário"""
        pass
    
    @abstractmethod
    def get_user(self, user_id: int) -> Dict:
        """Recupera dados de um usuário"""
        pass
    
    @abstractmethod
    def get_user_recommendations(self, user_id: int) -> List[Dict]:
        """Recupera recomendações de um usuário"""
        pass

class SQLiteStorage(DataStorage):
    """Implementação concreta para SQLite"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._create_tables()
    
    def _create_tables(self):
        """Cria as tabelas necessárias se não existirem"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Tabela de usuários
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    interests TEXT NOT NULL,
                    experience_level TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Tabela de recomendações
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS recommendations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    content TEXT NOT NULL,
                    type TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            conn.commit()
    
    def save_user(self, user_data: Dict) -> int:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO users (name, interests, experience_level) VALUES (?, ?, ?)',
                (user_data['name'], str(user_data['interests']), user_data['experience_level'])
            )
            conn.commit()
            return cursor.lastrowid
    
    def save_recommendation(self, user_id: int, recommendation_data: Dict) -> int:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO recommendations (user_id, content, type) VALUES (?, ?, ?)',
                (user_id, recommendation_data['content'], recommendation_data['type'])
            )
            conn.commit()
            return cursor.lastrowid
    
    def get_user(self, user_id: int) -> Dict:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
            user = cursor.fetchone()
            if user:
                return {
                    'id': user[0],
                    'name': user[1],
                    'interests': eval(user[2]),  # Converte string de volta para lista
                    'experience_level': user[3],
                    'created_at': user[4]
                }
            return {}
    
    def get_user_recommendations(self, user_id: int) -> List[Dict]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM recommendations WHERE user_id = ?', (user_id,))
            recommendations = cursor.fetchall()
            return [{
                'id': rec[0],
                'user_id': rec[1],
                'content': rec[2],
                'type': rec[3],
                'created_at': rec[4]
            } for rec in recommendations]

class StorageFactory(ABC):
    """Factory Method abstrato para criar storage"""
    
    @abstractmethod
    def create_storage(self) -> DataStorage:
        pass

class SQLiteStorageFactory(StorageFactory):
    """Factory concreto para criar SQLiteStorage"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
    
    def create_storage(self) -> DataStorage:
        return SQLiteStorage(self.db_path)
