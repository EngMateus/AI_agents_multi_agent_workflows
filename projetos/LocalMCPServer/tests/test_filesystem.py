### Teste para verificar se a camada do filesystem esta funcionando :: listagem, leitura e procura de arquivos na pasta definida esta funcionando 
### os arquivos que seram lidos, procurados e listados estão dentro da var DOCUMENTS_DIR



### funções do python importadas do src.tools.filesystem
from src.tools.filesystem import (
    list_files,
    read_file,
    search_files,
)


print("=== LISTA DE ARQUIVOS ===")

files = list_files()

for file in files:
    print(file)


print("\n=== LEITURA ===")

content = read_file("langchain.txt")

print(content)


print("\n=== BUSCA ===")

results = search_files("LangChain")

for result in results:
    print(result)