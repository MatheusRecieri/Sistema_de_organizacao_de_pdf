from fastapi import FastAPI # usada pra criar a web API a apartir de requisições HTTP e envia respostas em JSON
from services.file_scanner import scan_and_split  # importa a função de scanear diretorios

app = FastAPI() # a partir disso definir endpoints(rotas)

# definição da rota get
@app.get("/")
# servidor da aplicação
def root():
    return {"message:" "Servidor do ORganizador contábil rodando!"}

# define uma rota POST 
# recebe um json
@app.post("/processar")
def processar(payload: dict):
    caminho = payload.get("caminho") # pega o valor da chave "caminho"
    # verificação de cainho
    if not caminho:
        return {"erro": "Caminho não informado."}
    files_to_process = scan_and_split(caminho, split_pages=True)
    return {"status": "ok", "Total": len(files_to_process), "files": files_to_process}
