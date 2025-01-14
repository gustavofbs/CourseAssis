# Sistema de Suporte a Estudos

Um sistema completo para auxiliar estudantes em sua jornada de aprendizado, oferecendo planos de estudo personalizados e recomendações inteligentes.

## Funcionalidades Detalhadas

### Recomendações
- Sugestões de conteúdo baseadas no perfil
- Recomendações de materiais complementares
- Ajustes baseados no histórico de estudo

### Planos de Estudo
- Criação de planos personalizados baseados em objetivos
- Definição de metas e prazos
- Adaptação automática baseada no progresso

## Fluxo de Navegação

#### Página Principal

- O usuário escreve o seu nome
- Especifica os seus interesses de cursos
- Seleciona o seu nível de experiência

#### Retorno das Recomendações

- Depois que o usuário definiu os seus interesses e o seu nível, será possível interagir com três opções:

  - 1 - Ver o curso diretamente no site da Coursera
  - 2 - Fazer uma pergunta sobre um curso específico e receber um retorno da IA generativa
  - 3 - Elaborar um plano de estudos definindo a sua disponibilidade semanal

## Tecnologias Utilizadas

- Backend: FastAPI
- Frontend: HTML, CSS, JavaScript
- UI Framework: Bootstrap 5
- Banco de Dados: SQLite
- IA: OpenAI via LangChain
- Gerenciamento de Dependências: Poetry

## Pré-requisitos

- Python 3.12+
- Poetry para gerenciamento de dependências
- SQLite3
- Chave de API OpenAI válida

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/gustavofbs/CourseAssis
cd app
```

2. Instale as dependências usando Poetry:
```bash
poetry install
```

## Execução da Aplicação

1. Ative o ambiente virtual do Poetry:
```bash
poetry shell
```

2. Configure as variáveis de ambiente:
- Crie um arquivo `.env` na raiz do projeto
- Adicione suas configurações (exemplo):
```
OPENAI_API_KEY=sua_chave_api
```

3. Inicie a aplicação:
```bash
poetry run uvicorn main:app --reload
```

4. Acesse a aplicação em seu navegador:
```
http://localhost:8000
```

## Execução dos Testes

Para executar os testes unitários e de integração:

```bash
poetry run pytest
```

Para ver o relatório de cobertura de testes:
```bash
poetry run pytest --cov=app
```

## Estrutura do Projeto

```
CourseAssis/
├── app/
│   ├── patterns/        # Implementações de padrões de projeto
│   ├── static/          # Arquivos estáticos (CSS, JS)
│   └── templates/       # Templates HTML
├── tests/               # Testes automatizados
├── main.py              # Ponto de entrada da aplicação
├── pyproject.toml       # Configuração do Poetry e dependências
└── README.md            # README atual
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