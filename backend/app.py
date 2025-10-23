from fastapi import (
    FastAPI,
    HTTPException,
)  # usada pra criar a web API a apartir de requisições HTTP e envia respostas em JSON
from pydantic import BaseModel
from services.file_scanner import scan_directory
from services.run_full_pipeline import processar_pipeline
import os

# from services.file_scanner import scan_and_split  # importa a função de scanear diretorios

app = FastAPI()  # a partir disso definir endpoints(rotas)


class DiretorioRequest(BaseModel):
    caminho: str


# definição da rota get
@app.get("/")
# servidor da aplicação
async def root():
    return {"message:" "Servidor do ORganizador contábil rodando!"}


# define uma rota POST
# recebe um json
@app.post("/processar")
def processar_diretorio(dados: DiretorioRequest):
    caminho = dados.caminho

    print(caminho)

    if not os.path.exists(caminho):
        raise HTTPException(status_code=400, detail="Caminho informado não existe")

    try:
        resultado = processar_pipeline(caminho)

        return {
            "status": "sucesso",
            "menssagem": "Processamento conclído com sucesso",
            "detalhes": resultado,
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao procesar arquiovs {str(e)}"
        )
