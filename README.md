## Estrutura do Projeto

```
CourseAssis/
├── app/
│   ├── __pycache__/
│   ├── patterns/                               # Padrões utilizados na criação da aplicação
│   │   ├── __pycache__/
│   │   ├── dataStorage_factory.py
│   │   ├── recommendation_strategy.py
│   │   ├── studyPlan_template.py
│   │   └── userData_template.py
│   ├── static/
│   │   ├── css/
│   │   └── js/
│   ├── templates/                              # Interface web através do index.html
│   │   └── index.html
│   └── __init__.py
├── .gitignore
├── .python-version
├── data.db
├── main.py
├── poetry.lock
├── pyproject.toml
└── README.md
```

## Fase 1: Coleta de Dados do Usuário (Template Method)

### Interface de Entrada
- Interface web implementada com FastAPI e templates HTML
- Coleta de informações essenciais do usuário:
  - Nome do usuário
  - Interesses principais (Python, IA, Engenharia de Dados, etc.)
  - Nível de experiência (iniciante, intermediário, avançado)

### Padrão Template Method

O Template Method define o esqueleto de um algoritmo em uma classe base, permitindo que subclasses sobrescrevam etapas específicas do algoritmo sem alterar sua estrutura.

- Quando: Durante a implementação da lógica para validação e processamento dos dados de entrada.
- Por quê: Esse padrão permite criar um fluxo base de coleta de dados que pode ser estendido futuramente.
- Exemplo de uso: Validar diferentes tipos de entrada do usuário com passos definidos em uma classe abstrata.

### Implementação

```python
class UserDataCollector(ABC):
    def collect_data(self):  # Template Method
        self.collect_name()
        self.collect_interests()
        self.collect_experience_level()
        return self.get_user_data()
```

## Fase 2: Processamento e Persistência de Dados (Factory Method)

### Estrutura do Banco de Dados SQLite
- Tabela `users`: Armazena informações do usuário
- Tabela `recommendations`: Histórico de recomendações feitas

### Padrão Factory Method

O Factory Method fornece uma interface para criar objetos em uma superclasse, permitindo que subclasses alterem o tipo de objetos criados.

- Quando: Na criação de instâncias para diferentes estratégias de armazenamento
- Por quê: Facilita a mudança do banco de dados no futuro (ex: de SQLite para PostgreSQL)
- Exemplo de uso: Criar instâncias de conexões com o banco de dados

### Implementação

```python
class DataStorage(ABC):
    @abstractmethod
    def save_user(self, user_data: Dict) -> int:
        pass
    
    @abstractmethod
    def save_recommendation(self, user_id: int, recommendation_data: Dict) -> int:
        pass
```

## Fase 3: Recomendações Inteligentes (Strategy Pattern)

### Integração com LangChain e OpenAI
- Utilização do LangChain para interação com modelos de linguagem
- Implementação de prompts dinâmicos para recomendações personalizadas
- Geração de recomendações baseadas no perfil do usuário

### Padrão Strategy

O Strategy permite definir uma família de algoritmos de recomendação, encapsulando cada um e tornando-os intercambiáveis.

### Implementação

```python
class RecommendationStrategy:
    def generate_recommendations(self, user_data: Dict) -> Dict:
        # Gera recomendações usando LangChain e OpenAI
        pass
```

## Fase 4: Automação com Python

### Integração com APIs Externas
- Utilização da biblioteca `requests` para buscar informações de cursos
- Integração com plataformas de cursos online
- Apresentação formatada das recomendações

### Implementação
- Busca automática de informações atualizadas sobre cursos em relação a Coursera
- Formatação e apresentação clara dos resultados através de uma interface web

## Fase 5: Integração com IA Generativa

### Sistema de Perguntas e Respostas
- Permite que usuários façam perguntas sobre cursos recomendados
- Utiliza IA generativa para fornecer respostas contextualizadas
- Mantém histórico de interações

### Endpoint de Perguntas
```python
@app.post("/ask_question")
async def ask_question(question: str, course_context: Dict) -> str:
    # Processa perguntas sobre cursos usando IA
    pass
```

## Fase 6: Projeto Prático (Plano de Estudos)

### Geração de Plano de Estudos
- Criação de cronograma personalizado
- Divisão do conteúdo em etapas
- Adaptação ao tempo disponível do usuário

### Padrão Template Method para Planos
- Estrutura base para diferentes tipos de planos
- Personalização baseada no perfil e disponibilidade
- Distribuição otimizada do tempo de estudo

## API Endpoints

### Endpoints Principais

1. `GET /`
   - Retorna a página inicial da aplicação
   - Response: HTML

2. `POST /submit`
   - Submete dados do usuário e gera recomendações
   - Parameters:
     - `name`: string
     - `interests`: JSON string (array)
     - `experience_level`: string
   - Response: JSON com dados do usuário, ID e recomendações

3. `POST /ask_question`
   - Responde perguntas sobre cursos específicos
   - Parameters:
     - `question`: string
     - `course_name`: string
     - `course_description`: string
   - Response: JSON com a resposta

4. `POST /generate_study_plan`
   - Gera um plano de estudos personalizado
   - Parameters:
     - `course_name`: string
     - `course_description`: string
     - `weekly_hours`: integer
     - `start_date`: string
     - `end_date`: string
     - `fundamentals_percent`: integer
     - `development_percent`: integer
     - `project_percent`: integer
   - Response: JSON com o plano de estudos

## Tecnologias Utilizadas

- Backend: FastAPI
- Frontend: HTML, CSS, JavaScript
- UI Framework: Bootstrap 5
- Banco de Dados: SQLite
- IA: OpenAI via LangChain
- Gerenciamento de Dependências: Poetry

## Como Executar

1. Clone o repositório
```bash
git clone [URL_DO_REPOSITÓRIO]
```

2. Instale as dependências usando Poetry
```bash
cd app
poetry install
```

3. Ative o ambiente virtual do Poetry
```bash
poetry shell
```

4. Configure as variáveis de ambiente no arquivo `.env`
```bash
OPENAI_API_KEY=<YOUR_TOKEN>
```

5. Execute a aplicação
```bash
poetry run uvicorn main:app --reload
```

A aplicação estará disponível em `http://localhost:8000`

## Pré-requisitos

- Python 3.12+
- Poetry para gerenciamento de dependências
- SQLite3
- Chave de API OpenAI válida

## Aplicação

### Página inicial
![home](/assets/home.png)


### Recomendações geradas
![rec](/assets/rec.png)


### Campo para perguntas
![perguntaModal](/assets/perguntaModal.png)

### Resposta gerada
![perguntaResposta](/assets/perguntaResposta.png)

### Planejamento de plano de estudos
![studyPlan](/assets/studyPlan.png)

### Plano gerado
![studyPlanReturn](/assets/studyPlanReturn.png)