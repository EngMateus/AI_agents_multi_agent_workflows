# 🚀 Agentic AI & LLM Engineering: De Fundamentos a Sistemas Inteligentes

Repositório dedicado ao estudo, prática e desenvolvimento de aplicações orientadas a **Agentes de IA**, **LLMs** e **Orquestração de Dados**. Aqui documento minha evolução técnica, arquiteturas construídas e implementação de padrões de mercado utilizando o ecossistema Python.

---

## 🎯 Objetivo do Repositório

O propósito deste repositório é consolidar conceitos teóricos e práticos exercitados ao longo do curso **Complete Agentic AI Bootcamp With LangGraph and Langchain** (ministrado por **Krish Naik**). O objetivo é demonstrar a construção de pipelines eficientes de ingestão de dados, engenharia de contexto, saídas estruturadas e agentes autônomos prontos para produção.

---

## 🛠️ Tecnologias & Ferramentas

- **Linguagens & Manipulação de Dados:** Python 3.10+, NumPy, Pandas
- **Frameworks de IA & Orquestração:** LangChain (LCEL, Chains, Loaders), LangGraph (StateGraphs, ReAct), DeepAgents, AutoGen
- **Interfaces, APIs & Servidores:** FastAPI, Streamlit, LangServe, Model Context Protocol (MCP)
- **Provedores de LLMs & Modelos:** OpenAI API, Groq Cloud (LPU), Anthropic (Claude Ecosystem), Ollama (Modelos Locais), HuggingFace
- **Engenharia de Dados & Scraping:** BeautifulSoup4 (bs4), WebBaseLoader, TextLoader, Wikipedia API, Tavily Search API
- **Bancos Vetoriais & Busca:** ChromaDB, FAISS, Qdrant, Pinecone
- **Observabilidade & Avaliação:** LangSmith, LangGraph Studio, Guardrails, LLM Gateways
- **Desenvolvimento, Ambientes & CI/CD:** VS Code, Cursor IDE, Anaconda/Conda, UV Package Manager, Python-Dotenv, Git/GitHub, Postman
- **Deploy & Cloud:** Docker, AWS (ECS/Fargate), Render

---

---

## 🗺️ Visão de Aprendizado & Módulos Futuros (Bootcamp Roadmap)

### 🧠 RAG Avançado & Bancos Vetoriais
- **Embeddings & Vetores:** Transformação de texto em espaço vetorial e armazenamento em bancos vetoriais (ChromaDB/FAISS/Qdrant/Pinecone).
- **Estratégias de RAG:** Implementação de Agentic RAG, Corrective RAG (CRAG), Adaptive RAG e Vectorless RAG (PageIndex).
- **Retrieval Pipelines:** Busca por similaridade (Cosine, MMR) para recuperação de contextos relevantes sem alucinações.

### 🔄 Arquitetura de Agentes & Protocolos Avançados
- **StateGraphs & ReAct:** Modelagem de tomada de decisão com nós (*Nodes*), rotas condicionais (*Conditional Edges*) e estado compartilhado (`TypedDict`, `DataClass`, `Pydantic`).
- **Model Context Protocol (MCP):** Integração e criação de servidores MCP com ferramentas (tools) e clientes customizados.
- **Claude Ecosystem & Deep Agents:** Uso de sub-agentes, hooks, habilidades (skills) e plugins contextuais.
- **Human-in-the-Loop (HITL):** Pausas no fluxo para validação, edição e aprovação humana em tempo de execução.
- **Memória & Persistência:** Guardar histórico e estado do agente entre sessões com `Checkpointers`.

### 🤝 Multi-Agent Systems
- **Arquitetura Supervisor & Orchestrator-Worker:** Agente gerente que coordena e delega sub-tarefas para agentes especialistas.
- **Orquestração Paralela & Iterativa:** Execução paralela de agentes e loops de avaliação com padrões Evaluator-Optimizer.

### 🚀 Observabilidade, Deploy & Produção
- **LangSmith & LangGraph Studio:** Tracing completo de chamadas, latência, consumo de tokens, simulações e debugging de agentes.
- **Deploy & Cloud:** Criação de interfaces com Streamlit, APIs REST com FastAPI/LangServe, containerização com Docker e hospedagem em cloud (AWS/Render).

---

## 🎓 Créditos & Referências

- **Curso:** Complete Agentic AI Bootcamp With LangGraph and Langchain
- **Instrutor:** Krish Naik - Chief AI Engineer
