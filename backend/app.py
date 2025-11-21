from fastapi import (
    FastAPI,
    HTTPException,
)  # usada pra criar a web API a apartir de requisições HTTP e envia respostas em JSON
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from services.file_scanner import scan_directory
from services.run_full_pipeline import processar_pipeline
import os

# from services.file_scanner import scan_and_split  # importa a função de scanear diretorios

app = FastAPI()  # a partir disso definir endpoints(rotas)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",  # caso use outra porta
    ],
    allow_credentials=True,
    allow_methods=["*"],  # Permite GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],  # Permite todos os headers
    expose_headers=["*"],  # Expõe todos os headers na resposta
)


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

        # ajuste para compatibilizar com o frontend
        resposta = {
            "status": "sucesso",
            "menssagem": "Processamento conclído com sucesso",
            "files": (
                resultado.get("notas-fiscais", [])
                + resultado.get("recibos", [])
                + resultado.get("outros", [])
            ),  # concatena e devolve como "files"
            "results": resultado.get("erros", []),  # detalhes com erros ou extrações
            "Total": resultado.get("total-processados", 0),  # número total
        }

        return resposta

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao procesar arquiovs {str(e)}"
        )
