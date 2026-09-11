# MCP File Server

> Um MCP Server em Python que fornece acesso controlado e somente leitura a documentos de texto para agentes de IA, utilizando Model Context Protocol, LangChain e Groq.

## Visão Geral

Este projeto demonstra como construir um **MCP Server** que permite a um agente de IA (LLM) listar, ler e buscar conteúdo dentro de documentos de texto de forma segura e padronizada.

O agente recebe perguntas em linguagem natural e decide automaticamente qual ferramenta usar para responder, graças ao **Tool Calling** integrado.

## Funcionalidades

- **Listar arquivos** — Mostra todos os documentos disponíveis no diretório
- **Ler conteúdo** — Acessa o conteúdo de um arquivo específico
- **Buscar texto** — Procura uma palavra ou expressão dentro dos documentos
- **Proteção contra path traversal** — Impede acesso a arquivos fora do diretório permitido
- **CLI interativo** — Interface de chat via terminal com o agente
- **System Prompt** — Persona do agente restrita ao escopo de arquivos

## Arquitetura

```
┌─────────────────────────────────────────────────────────┐
│                     USUÁRIO                             │
│                  (terminal CLI)                         │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│                  MCP CLIENT                             │
│                   client.py                             │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────────┐  │
│  │  ChatGroq   │  │  MCPAdapter  │  │ System Prompt │  │
│  │  (LLM)      │  │  (Bridge)    │  │ (Persona)     │  │
│  └─────────────┘  └──────┬───────┘  └───────────────┘  │
└──────────────────────────┼──────────────────────────────┘
                           │
                    MCP Protocol (stdio)
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│                  MCP SERVER                             │
│                src/server.py                            │
│              FastMCP "File Server"                      │
│  ┌─────────────────────────────────────────────────┐    │
│  │  @mcp.tool()                                    │    │
│  │  ├── get_files()        → lista arquivos        │    │
│  │  ├── get_file_content() → lê conteúdo           │    │
│  │  └── search_documents() → busca texto           │    │
│  └─────────────────────────────────────────────────┘    │
└──────────────────────────┬──────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│              TOOLS (funções Python)                     │
│            src/tools/filesystem.py                      │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────────┐  │
│  │ list_files()│  │ read_file()  │  │ search_files() │  │
│  └─────────────┘  └──────────────┘  └───────────────┘  │
└──────────────────────────┬──────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│              CONFIGURAÇÃO                               │
│               src/config.py                             │
│  ┌─────────────────────────────────────────────────┐    │
│  │  • Carrega variáveis do .env                    │    │
│  │  • Define BASE_DIR (raiz do projeto)            │    │
│  │  • Define DOCUMENTS_DIR (pasta de documentos)   │    │
│  └─────────────────────────────────────────────────┘    │
└──────────────────────────┬──────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│                DOCUMENTOS                               │
│              data/documents/                            │
│  ┌───────────────┐ ┌───────────────┐ ┌───────────────┐  │
│  │ langchain.txt │ │ langgraph.txt │ │    mcp.txt    │  │
│  └───────────────┘ └───────────────┘ └───────────────┘  │
└─────────────────────────────────────────────────────────┘
```

## Tecnologias

| Tecnologia | Versão | Uso no Projeto |
|------------|--------|----------------|
| Python | 3.12 | Linguagem principal |
| MCP | 2.2 | Protocolo de comunicação |
| FastMCP | 4.0 | Servidor MCP |
| LangChain | 1.4 | Framework do agente |
| LangChain Groq | 1.1 | Integração com LLM |
| Groq | - | Host da LLM |

## Pré-requisitos

- Python 3.12+
- Conta no [Groq](https://console.groq.com) (para obter API key)

## Instalação

### 1. Clonar o repositório

```bash
git clone https://github.com/EngMateus/AI_agents_multi_agent_workflows.git
cd AI_agents_multi_agent_workflows/projetos/LocalMCPServer
```

### 2. Criar ambiente virtual

```bash
python -m venv ambienteMCPServer
ambienteMCPServer\Scripts\activate  # Windows
# source ambienteMCPServer/bin/activate  # Linux/Mac
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar variáveis de ambiente

```bash
cp .env.example .env
```

Edite o arquivo `.env` e insira sua chave de API do Groq:

```
GROQ_API_KEY=sua_chave_aqui
```

## Execução

```bash
python client.py
```

O client lança o server automaticamente como subprocesso via stdio.

## Como Usar

Após iniciar o client, digite suas perguntas em linguagem natural:

```
MCP Client iniciado. Digite 'sair' para sair.

Você: Liste os arquivos disponíveis

Agente: Os arquivos disponíveis são: langchain.txt, langgraph.txt, mcp.txt

Você: O que o arquivo langchain.txt diz?

Agente: O arquivo langchain.txt diz o seguinte: LangChain é um framework...

Você: Onde aparece a palavra "estado"?

Agente: A palavra "estado" aparece em langgraph.txt na linha 7...

Você: Qual a capital da França?

Agente: Só posso ajudar com arquivos e documentos.

Você: sair
```

---

## Explicação dos Scripts

### `client.py` — MCP Client + Agente

Este é o **ponto de entrada principal** do projeto. Ele orquestra a comunicação entre o usuário, o agente LLM e o MCP Server.

**O que faz:**

1. **Conecta ao MCP Server** — Usa `MCPAdapter` para lançar `src/server.py` como subprocesso via stdio e descobrir as tools disponíveis
2. **Configura o LLM** — Instancia o `ChatGroq` com o modelo configurado
3. **Cria o agente** — Usa `create_agent()` do LangChain para combinar LLM + tools + system prompt
4. **Loop interativo** — Recebe perguntas do usuário via terminal e retorna respostas do agente

**Fluxo de execução:**

```
MCPAdapter(SERVER_PATH)
    → Lança src/server.py como subprocesso
    → Conecta via stdio
    → Descobre: get_files, get_file_content, search_documents

ChatGroq(model="openai/gpt-oss-20b")
    → Configura o LLM que vai "pensar" e decidir qual tool usar

create_agent(llm, tools, system_prompt)
    → Cria o agente com persona "File Assistant"
    → Restringe respostas ao escopo de arquivos

Loop:
    → Usuário digita pergunta
    → Agente decide: usar tool ou responder diretamente
    → Se tool: invoca via MCP → server executa → resultado volta
    → Agente formata resposta em linguagem natural
    → Exibe para o usuário
```

---

### `src/server.py` — MCP Server

Este script é o **coração do projeto** — ele transforma funções Python comuns em ferramentas MCP que qualquer cliente pode consumir.

**O que faz:**

1. **Configura o path** — Adiciona o diretório raiz ao `sys.path` para que os imports funcionem
2. **Cria o servidor** — Instancia `FastMCP("File Server")`
3. **Registra as tools** — Usa o decorador `@mcp.tool()` para registrar 3 funções como tools MCP
4. **Inicia o servidor** — `mcp.run()` começa a escutar via stdio

**As 3 tools registradas:**

| Tool MCP | Função Python | Descrição |
|----------|---------------|-----------|
| `get_files()` | `list_files()` | Lista todos os arquivos no diretório de documentos |
| `get_file_content(filename)` | `read_file(filename)` | Lê o conteúdo de um arquivo específico |
| `search_documents(query)` | `search_files(query)` | Busca uma palavra/expressão nos documentos |

**Como o registro funciona:**

```python
mcp = FastMCP("File Server")  # Cria o servidor

@mcp.tool()                    # Registra como tool MCP
def get_files() -> list[str]:  # Type hints → schema automático
    """Docstring → descrição da tool"""  # Docstring → descrição
    return list_files()        # Chama a função Python
```

O `FastMCP` gera automaticamente o JSON Schema das tools a partir dos type hints e docstrings, seguindo o protocolo MCP.

---

### `src/tools/filesystem.py` — Funções de Filesystem

Este script contém as **funções Python puras** que implementam a lógica de manipulação de arquivos. Elas são independentes do MCP — poderiam ser usadas sem o protocolo.

**Funções implementadas:**

#### `list_files() → list[str]`

- Usa `DOCUMENTS_DIR.rglob("*")` para encontrar todos os arquivos recursivamente
- Retorna caminhos relativos ao diretório de documentos
- Exemplo de retorno: `["langchain.txt", "langgraph.txt", "mcp.txt"]`

#### `read_file(filename: str) → str`

- Valida se o arquivo está dentro do diretório permitido (proteção contra path traversal)
- Verifica se o arquivo existe e é um arquivo (não um diretório)
- Retorna o conteúdo do arquivo como string

**Segurança:**

```python
file_path = (DOCUMENTS_DIR / filename).resolve()
if not file_path.is_relative_to(DOCUMENTS_DIR):
    raise ValueError("Acesso ao arquivo não permitido.")
```

Isso impede que um atacante use `../../etc/passwd` para acessar arquivos fora do diretório permitido.

#### `search_files(query: str) → list[dict]`

- Converte a busca para minúsculas (case-insensitive)
- Percorre todos os arquivos do diretório
- Para cada linha, verifica se a query aparece
- Retorna lista de dicionários com: `file`, `line`, `content`

**Exemplo de retorno:**

```python
[
    {"file": "langchain.txt", "line": 1, "content": "LangChain é um framework..."},
    {"file": "mcp.txt", "line": 1, "content": "MCP significa Model Context Protocol..."}
]
```

---

### `src/config.py` — Configuração

Centraliza todas as configurações de caminhos e variáveis de ambiente.

**O que faz:**

1. **Carrega `.env`** — Usa `python-dotenv` para ler variáveis de ambiente
2. **Define `BASE_DIR`** — Caminho absoluto da raiz do projeto
3. **Define `DOCUMENTS_DIR`** — Caminho absoluto da pasta de documentos
4. **Garante existência** — Cria o diretório de documentos se não existir

**Variáveis utilizadas:**

| Variável | Origem | Valor padrão |
|----------|--------|--------------|
| `DOCUMENTS_PATH` | `.env` | `./data/documents` |

**Fluxo:**

```
.env → load_dotenv() → os.getenv("DOCUMENTS_PATH")
    → BASE_DIR / DOCUMENTS_PATH → DOCUMENTS_DIR
    → mkdir(parents=True, exist_ok=True)
```

---

### `tests/test_filesystem.py` — Testes

Script de teste manual para verificar se as funções do filesystem estão funcionando corretamente.

**O que testa:**

1. **Listagem** — Chama `list_files()` e imprime os arquivos encontrados
2. **Leitura** — Chama `read_file("langchain.txt")` e imprime o conteúdo
3. **Busca** — Chama `search_files("LangChain")` e imprime os resultados

**Como rodar:**

```bash
python tests/test_filesystem.py
```

> **Nota:** Este é um teste manual (sem framework). Para testes automatizados, considere adicionar `pytest`.

---

## Ferramentas MCP Disponíveis

| Tool | Descrição | Parâmetros | Retorno |
|------|-----------|------------|---------|
| `get_files()` | Lista todos os arquivos no diretório de documentos | Nenhum | `list[str]` |
| `get_file_content(filename)` | Lê o conteúdo de um arquivo específico | `filename`: nome do arquivo | `str` |
| `search_documents(query)` | Busca uma palavra/expressão nos documentos | `query`: texto a ser buscado | `list[dict]` |

---

## Estrutura do Projeto

```
LocalMCPServer/
├── client.py              # MCP Client + Agente LangChain
├── src/
│   ├── server.py          # MCP Server (FastMCP)
│   ├── config.py          # Configuração de caminhos
│   └── tools/
│       └── filesystem.py  # Funções de listagem, leitura e busca
├── data/
│   └── documents/         # Documentos de exemplo
│       ├── langchain.txt
│       ├── langgraph.txt
│       └── mcp.txt
├── tests/
│   └── test_filesystem.py # Testes das funções filesystem
├── requirements.txt       # Dependências Python
├── .env.example           # Template de variáveis de ambiente
├── .gitignore             # Arquivos ignorados pelo Git
└── README.md              # Este arquivo
```

---

## Conceitos Estudados

| Conceito | Onde aparece no código |
|----------|----------------------|
| **Model Context Protocol (MCP)** | Protocolo inteiro — `mcp`, `FastMCP` |
| **MCP Server** | `src/server.py` — `@mcp.tool()` |
| **MCP Client** | `client.py` — `MCPAdapter` |
| **MCP Tools** | `get_files`, `get_file_content`, `search_documents` |
| **LangChain** | Criação do agent, integração com tools |
| **Tool Calling** | LLM decide quando usar cada tool |
| **Segurança** | Path traversal guard em `read_file()` |

---

## Segurança

O projeto implementa proteção contra **path traversal** na função `read_file()`:

```python
file_path = (DOCUMENTS_DIR / filename).resolve()
if not file_path.is_relative_to(DOCUMENTS_DIR):
    raise ValueError("Acesso ao arquivo não permitido.")
```

Isso garante que o agente só possa acessar arquivos dentro do diretório `data/documents/`.

---

## Dependências

| Pacote | Função |
|--------|--------|
| `mcp` | SDK oficial do protocolo MCP |
| `python-dotenv` | Carrega variáveis do `.env` |
| `langchain[mcp]` | `MCPAdapter` + `create_agent` |
| `langchain-groq` | `ChatGroq` (LLM via Groq) |

---

## Licença

Este é um projeto de estudo e prática.
