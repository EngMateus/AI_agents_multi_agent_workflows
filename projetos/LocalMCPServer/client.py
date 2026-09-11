import asyncio
from pathlib import Path

from langchain.agents import create_agent
from langchain.mcp import MCPAdapter
from langchain_groq import ChatGroq


from dotenv import load_dotenv

load_dotenv()

SERVER_PATH = Path("src/server.py")



## aqui aonde o meu agent atua para usar do meu MCP server
## MCPAdapter -> é a classe responsável por descobrir as ferramentas de um servidor MCP e adapta-las  para que funcionem dentro de um agente 
### Server_path -> caminho aonde meu servidor esta e dali que o MCPAdpater puxa as tools

async def main():
    async with MCPAdapter(SERVER_PATH) as adapter:
        ### as tools que vem do MCP servem ficam aqui nessa var
        tools = await adapter.list_tools()
        llm = ChatGroq(
            model="openai/gpt-oss-20b"
        )

        agent = create_agent(
            model=llm,
            tools=tools,
            system_prompt = """Você é um assistente de arquivos chamado File Assistant.

            Suas únicas capacidades são:
            - Listar arquivos disponíveis no diretório de documentos
            - Ler o conteúdo de um arquivo específico
            - Buscar uma palavra ou expressão dentro dos documentos

            REGRAS ESTRTITAS:
            1. Responda APENAS sobre assuntos relacionados aos arquivos e documentos disponíveis.
            2. NÃO responda perguntas gerais, curiosidades, opiniões, ou assuntos fora do escopo.
            3. Se o usuário perguntar algo fora do escopo, responda educadamente que você só pode ajudar com arquivos e documentos.
            4. Use SEMPRE as tools disponíveis para responder. Não invente conteúdo.
            5. Se não encontrar um arquivo ou termo, diga que não encontrou.""",
            )

        print("MCP Client iniciado. Digite 'sair' para sair.\n")

        while True:
            query = input("Você: ")

            if query.lower() in ("sair", "exit", "quit"):
                break

            response = await agent.ainvoke(
                {"messages": [{"role": "user", "content": query}]}
            )

            print(f"\nAgente: {response['messages'][-1].content}\n")


if __name__ == "__main__":
    asyncio.run(main())
