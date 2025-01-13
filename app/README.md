## Estrutura do Projeto

```
app/
├── app/
│   ├── patterns/
│   │   └── template_method.py    # Implementação do Template Method
│   ├── static/
│   │   └── css/
│   │       └── style.css         # Estilos da aplicação
│   ├── templates/
│   │   └── index.html            # Template da interface web
│   └── main.py                   # Aplicação FastAPI
├── pyproject.toml                # Dependências do projeto
└── README.md                     # Este arquivo
```

## Padrão Template Method

O Template Method é um padrão de projeto comportamental que define o esqueleto de um algoritmo em uma classe base, permitindo que subclasses sobrescrevam etapas específicas do algoritmo sem alterar sua estrutura.

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