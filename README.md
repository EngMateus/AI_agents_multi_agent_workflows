🚀 Agentic AI & LLM Engineering: De Fundamentos a Sistemas Inteligentes
Repositório dedicado ao estudo, prática e desenvolvimento de aplicações orientadas a Agentes de IA, LLMs e Orquestração de Dados. Aqui documento minha evolução técnica, arquiteturas construídas e implementação de padrões de mercado utilizando o ecossistema Python.

🎯 Objetivo do Repositório
O propósito deste repositório é consolidar conceitos teóricos e práticos do ecossistema de AI Engineering, demonstrando a construção de pipelines eficientes de ingestão de dados, engenharia de contexto, saídas estruturadas e agentes autônomos.

🛠️ Tecnologias & Ferramentas
Linguagem: Python 3.10+

Frameworks de IA: LangChain, LangGraph, Pydantic (V2)

Provedores de LLM & Inferência: OpenAI API, Groq Cloud (LPU), Ollama (Modelos Locais)

Manipulação de Dados & Scraping: BeautifulSoup4 (bs4), WebBaseLoader, TextLoader, Wikipedia API

Ambiente & Configuração: Python-Dotenv, Conda, Virtualenv

📚 Módulos & Tópicos Práticos
1. Garantia de Tipos & Structured Output (Pydantic V2)
Modelagem de Dados: Criação de schemas com BaseModel e validação estrita com Field.

Dynamic Defaults: Utilização de default_factory para valores dinâmicos por instância.

JSON Schema Generation: Exportação de esquemas via model_json_schema() para passar instruções precisas de Structured Outputs e Function Calling para LLMs.

2. Infraestrutura de LLMs & Provedores
Multi-Provider Setup: Alternância entre provedores proprietários (OpenAI) e de alta performance/open-weights (Groq).

Gestão de Custos & Latência: Execução de modelos abertos (Llama 3.3 70B, DeepSeek R1, GPT-OSS) com cota gratuita via Groq API.

Gerenciamento de Segredos: Manipulação segura de chaves de API com python-dotenv.

3. Ingestão de Dados (Document Loaders)
Documentos Locais: Carregamento de arquivos estruturados e não estruturados (TextLoader) com validação de encodagem utf-8 e manipulação via pathlib.Path.

Web Scraping Otimizado: Extração de conteúdo web via WebBaseLoader integrado ao BeautifulSoup4.

Filtros por HTML/CSS: Uso do bs4.SoupStrainer (com class_ e name) para extração direcionada, reduzindo ruído e economizando tokens de contexto.

Simulação de Navegador: Customização de requisições HTTP (header_template com User-Agent) para contornar bloqueios de scraping (ex: Yahoo Finance, Medium).

APIs de Conhecimento: Integração com WikipediaLoader configurado para busca de conceitos e metadados.

4. Engenharia de Texto & Estratégias de Chunking
Divisão Recursiva de Texto: Segmentação de documentos densos com RecursiveCharacterTextSplitter.

Preservação Semântica: Uso de separadores hierárquicos (\n\n, \n,  ) para evitar a quebra de palavras e frases no meio.

Janelas de Sobreposição (Overlap): Configuração de chunk_size (limite máximo) e chunk_overlap para manter a continuidade do contexto na transição de blocos para RAG.
