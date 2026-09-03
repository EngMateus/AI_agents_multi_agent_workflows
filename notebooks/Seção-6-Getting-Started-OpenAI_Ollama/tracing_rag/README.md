![Fluxo de Depuração no LangSmith](rag_langsmith_foto/RagDepuracaoLangSmith.png)


# 🚀 Documentação e Análise do Trace no LangSmith — Projeto RAG

Este documento detalha o fluxo de execução (*Trace*) do projeto **RAG com LangChain, ChromaDB e Groq**, analisado por meio da ferramenta de observabilidade **LangSmith**.

---

## 📌 Visão Geral da Execução
* **Cadeia Executada:** RAG básico (Vector Search + Prompt Templates + Chat Model + Output Parser)
* **Tempo Total de Resposta:** `1.95s`
* **Consumo Total de Tokens:** `821 tokens`
* **Modelo Utilizado:** `openai/gpt-oss-120b` (via Groq API)

---

## 🏗️ Anatomia do Workflow e Seus Nós (*Nodes*)

### 1. `RunnableSequence` (Nó Raiz / Chain)
* **Métricas:** `1.95s` | `821 tokens`
* **O que faz:** É o container principal que agrupa toda a pipeline encadeada pelo operador `|` (`rag_chain = { ... } | prompt | modelo | StrOutputParser()`). Mede o tempo total do início ao fim da requisição.

---

### 2. `RunnableParallel<context,question>`
* **Métricas:** `0.19s`
* **O que faz:** Responsável por preparar as entradas do prompt **em paralelo**, dividindo a execução em duas tarefas simultâneas:
  * **Rota 1 (`context`):** Busca documentos no banco de vetores.
  * **Rota 2 (`question`):** Preserva a pergunta original do usuário.
* **Saída:** Um dicionário Python com a estrutura `{"context": "...", "question": "..."}`.

#### ↳ Sub-nós da Rota `context`:
* **`map:key:context` (`0.19s`):** Nó pai responsável por gerenciar o processamento da chave `context`.
* **`VectorStoreRetriever` (`0.18s`):** Consulta o **ChromaDB** usando embeddings (`nomic-embed-text`) e recupera os $k=3$ chunks com maior similaridade semântica com a pergunta.
* **`format_docs` (`0.00s`):** Função auxiliar Python que concatena a lista de documentos recuperados pelo retriever em uma única *string*.

#### ↳ Sub-nó da Rota `question`:
* **`RunnablePassthrough` (`0.00s`):** Atua como uma "ponte" transparente, repassando a pergunta digitada no `.invoke()` sem qualquer alteração.

---

### 3. `ChatPromptTemplate`
* **Métricas:** `0.00s`
* **O que faz:** Mapeia dinamicamente o dicionário recebido do `RunnableParallel` dentro dos *placeholders* `{context}` e `{question}`.
* **Saída:** Estrutura de mensagens pronta para a API de Chat:
  * **SystemMessage:** Instruções de comportamento do agente + blocos de contexto injetados.
  * **HumanMessage:** Pergunta original do usuário.

---

### 4. `ChatGroq` (`openai/gpt-oss-120b`)
* **Métricas:** `1.65s` | `821 tokens`
* **O que faz:** Requisição HTTP externa para os servidores da Groq. O modelo recebe as mensagens do `ChatPromptTemplate`, analisa o contexto injetado para evitar alucinações e gera a resposta autoregressivamente.
* **Observação:** Representa o maior gargalo de latência do fluxo ($\approx 84\%$ do tempo total).

---

### 5. `StrOutputParser`
* **Métricas:** `0.00s`
* **O que faz:** Recebe o objeto bruto `AIMessage` retornado pelo `ChatGroq` e extrai apenas a propriedade `.content` (texto puro), descartando metadados e entregando o resultado final da cadeia.

---

## 📈 Tabela Resumo de Performance

| Nó | Tipo de Operação | Duração | Custo/Tokens |
| :--- | :--- | :--- | :--- |
| **`RunnableSequence`** | Container Geral | 1.95s | 821 tokens |
| **`RunnableParallel`** | Processamento de Dados | 0.19s | - |
| **`VectorStoreRetriever`** | Busca Vetorial (ChromaDB) | 0.18s | - |
| **`ChatPromptTemplate`** | Formatação de String | 0.00s | - |
| **`ChatGroq`** | Chamada de API (LLM) | 1.65s | 821 tokens |
| **`StrOutputParser`** | Extração de Texto | 0.00s | - |

---

## 💡 Principais Aprendizados
1. **Redução de Alucinações:** A injeção do contexto recuperado via `VectorStoreRetriever` garante que o modelo responda estritamente com base nos dados do documento.
2. **Eficiência no Tratamento de Dados:** As tarefas de busca de contexto e repasse de perguntas rodando em paralelo reduzem o tempo de preparação do prompt para menos de $0.2\text{s}$.
3. **Análise de Gargalos:** O rastreamento no LangSmith comprova que o foco para otimização de latência deve ser a escolha/parametrização do LLM (`ChatGroq`), já que o tempo de infraestrutura e recuperação de dados local é irrelevante frente ao tempo de geração do modelo.
