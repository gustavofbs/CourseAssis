## Estrutura do Projeto

```
app/
├── app/
│   ├── patterns/
│   │   ├── template_method.py    # Implementação do Template Method
│   │   └── factory_method.py     # Implementação do Factory Method
│   ├── static/
│   │   └── css/
│   │       └── style.css         # Estilos da aplicação
│   ├── templates/
│   │   └── index.html            # Template da interface web
│   └── main.py                   # Aplicação FastAPI
├── pyproject.toml                # Dependências do projeto
└── README.md                     # Este arquivo
```

## Fase 1: Coleta de Dados (Template Method)

### Padrão Template Method

O Template Method é um padrão de projeto comportamental que define o esqueleto de um algoritmo em uma classe base, permitindo que subclasses sobrescrevam etapas específicas do algoritmo sem alterar sua estrutura.

- Quando: Durante a implementação da lógica para validação e processamento dos dados de entrada.
- Por quê: Esse padrão permite criar um fluxo base de coleta de dados (e.g., validação, persistência) que pode ser estendido ou ajustado futuramente.
- Exemplo de uso: Validar diferentes tipos de entrada do usuário (nome, interesses, nível) com passos definidos em uma classe abstrata.

### Implementação

#### Classe Abstrata Base (`UserDataCollector`)
```python
class UserDataCollector(ABC):
    def collect_data(self):  # Template Method
        self.collect_name()
        self.collect_interests()
        self.collect_experience_level()
        return self.get_user_data()
```

- Define a sequência de passos para coleta de dados
- Métodos abstratos que devem ser implementados pelas subclasses:
  - `collect_name()`
  - `collect_interests()`
  - `collect_experience_level()`
  - `get_user_data()`

#### Implementação Concreta (`WebUserDataCollector`)
- Implementa a coleta de dados específica para ambiente web
- Armazena dados em um dicionário estruturado
- Integra-se com o frontend através da API FastAPI

## Fase 2: Processamento e Persistência de Dados (Factory Method)

### Padrão Factory Method

O Factory Method é um padrão criacional que fornece uma interface para criar objetos em uma superclasse, mas permite que as subclasses alterem o tipo de objetos que serão criados.

- Quando: No momento de criar instâncias específicas para diferentes estratégias de armazenamento ou integração com o banco de dados.
- Por quê: Ajuda a encapsular a lógica de criação de objetos (e.g., tabelas, conexões), tornando mais fácil mudar o banco de SQLite para outro no futuro, como PostgreSQL.
- Exemplo de uso: Criar uma fábrica para produzir instâncias de tabelas ou conexões com o banco de dados com base em configurações.

### Implementação

#### Interface de Armazenamento (`DataStorage`)
```python
class DataStorage(ABC):
    @abstractmethod
    def save_user(self, user_data: Dict) -> int:
        pass
    
    @abstractmethod
    def save_recommendation(self, user_id: int, recommendation_data: Dict) -> int:
        pass
```

#### Factory Method
```python
class StorageFactory(ABC):
    @abstractmethod
    def create_storage(self) -> DataStorage:
        pass

class SQLiteStorageFactory(StorageFactory):
    def create_storage(self) -> DataStorage:
        return SQLiteStorage(self.db_path)
```

### Estrutura do Banco de Dados

#### Tabela Users
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    interests TEXT NOT NULL,
    experience_level TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

#### Tabela Recommendations
```sql
CREATE TABLE recommendations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    content TEXT NOT NULL,
    type TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
)
```

Nota: O SQLite cria automaticamente uma tabela `sqlite_sequence` para gerenciar os IDs autoincrementais, garantindo que sejam únicos e sempre crescentes, mesmo após deleções.

## Tecnologias Utilizadas

- Backend: FastAPI
- Frontend: HTML, CSS, JavaScript
- UI Framework: Bootstrap 5
- Gerenciamento de Dependências: Poetry

## Como Executar

1. Instale as dependências:
```bash
poetry install
```

2. Inicie o servidor:
```bash
poetry run uvicorn app.main:app --reload
```

3. Acesse a aplicação em `http://localhost:8000`