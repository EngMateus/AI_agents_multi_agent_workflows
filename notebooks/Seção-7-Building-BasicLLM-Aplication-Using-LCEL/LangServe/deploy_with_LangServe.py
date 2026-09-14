### LangServe -> expor meu agente em um swagger documentado, usa FastAPI() para lançar
### serve para fazer um rápido deploy e possibilitar de forma rápida, sistemas consumirem meu fluxo agentico
### Métodos POST e GET por padrão 
### POST -> invoke() ;; batch() ;; stream() ;; stream_log() 
### GET -> input_schema() ;; output_schema() ;; config_schema() 


### -> Ao criar uma aplicação agentica usando LCEL de maneira rápida, o próximo passo e disponibilizar esse sistema para usuários poderem dar seus feedbacks
###  ideia + lCEL = protótipo ;; protótipo + langServe = API pronta para produção
### API pronta para produção + provedor de hospedagens = implantação em produção + tracing = Monitoramento em produção


from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.messages import HumanMessage
from langserve import add_routes
from fastapi import FastAPI
from pprint import pprint 


model = init_chat_model(
    model_provider = 'groq',
    model = 'openai/gpt-oss-20b',
    temperature = 0.50
)

system_template = "Translate the fallowing into {language}"
prompt_template = ChatPromptTemplate.from_messages([
    ('system',system_template),
        ('user','{text}')
])


### parseador 
parser = StrOutputParser()


### chain
chain = prompt_template | model | parser



### definição do APP
app = FastAPI(
    ### dados aqui servem mais para documentação da minha aplicaçao
    ### version 1.0, posso indo incrementando conforme novas melhororias, correções .....
    title="LangChain Server",
    version="1.0",
    description="A Simple API Server using LangChain runnable interfaces"
)

### adicionando as rotas da chain
add_routes(
    app,
    chain,
    ### ao definir esse path=chain, ele pega os métodos da chain e joga no swagger tambem
    path="/chain"
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,host="localhost",port=8000)