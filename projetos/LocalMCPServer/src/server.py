### O SCRIPT SRC.TOOL.FILESYSTEM.PY É APENAS AONDE DE INICIO, AS FUNÇÕES DO PYTHON ESTÃO CRIADAS, SÃO SERAM TRANFORMADAS EM MCP TOOLS AQUI DENTRO DESSE SCRIPT
### IMPORTA TODOS AS FUNÇÕES COMO LIST_FILES();;READ_FILES();;SEARCH_FILES() AQUI 



import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastmcp import FastMCP

from src.tools.filesystem import (
    list_files,
    read_file,
    search_files,
)


# Cria o MCP Server e definido como 'File Server' como o nome do servidor
### ao intanciar o nosso servidor mcp, devemos logo em seguida, registrar quais são as capacidades que o nosso mcv server tera
### para tools, devemnos usar @mpc.tool() (decorador) e logo abaixo, a função que importamos do src.tool.filesystem
### devemos definir uma boa docstring, nesse caso, docs strings ficaram basicas pois, se tratam de tools básicas, aonde não temos muita complexidade
### objetivo aqui, é entender como o MCP funciona

### todas os mcp.tool aqui, nos diz que, o nosso servidor vai disponibilizar esssas tools para seus clientes
### 
mcp = FastMCP("File Server")


@mcp.tool()
def get_files() -> list[str]:
    """
    Lista todos os arquivos disponíveis
    no diretório de documentos.
    """

    return list_files()


@mcp.tool()
def get_file_content(filename: str) -> str:
    """
    Lê o conteúdo de um arquivo específico.

    Args:
        filename: Caminho do arquivo dentro
                  do diretório de documentos.
    """

    return read_file(filename)


@mcp.tool()
def search_documents(query: str) -> list[dict]:
    """
    Procura uma palavra ou expressão
    dentro dos documentos disponíveis.

    Args:
        query: Texto que será pesquisado.
    """

    return search_files(query)


if __name__ == "__main__":
    mcp.run()



### mcp run() -> inicia o servidor
### fluxo -> FastMCP() -> mcp.tools -> mcp.run() ---> aguarda por um mcp Cliente consumir