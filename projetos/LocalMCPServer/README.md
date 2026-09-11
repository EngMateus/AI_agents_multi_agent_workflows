# MCP File Server

MCP Server desenvolvido em Python para disponibilizar acesso
controlado a arquivos para aplicações de Inteligência Artificial.

## Objetivo

Este projeto tem como objetivo estudar:

- Model Context Protocol (MCP)
- MCP Server
- MCP Tools
- MCP Client
- LangChain
- LangGraph
- Tool Calling
- Segurança
- Observabilidade

## Arquitetura

```text
MCP Client
    |
    | MCP
    v
MCP Server
    |
    +-- get_files()
    |
    +-- get_file_content()
    |
    +-- search_documents()
    |
    v
data/documents/