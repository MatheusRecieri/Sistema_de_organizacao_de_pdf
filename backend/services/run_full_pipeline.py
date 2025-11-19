import os
from services.splitter_pdf import split_pdf_by_page
from services.extractor_pdf import extract_pdf_data
from services.organizer import organize_files_parallel


def processar_pipeline(base_directory):
    resultados = {
        "total-processados": 0,
        "notas-fiscais": [],
        "recibos": [],
        "outros": [],
        "erros": [],
    }

    if not os.path.isdir(base_directory):
        raise ValueError(f"O caminho {base_directory} não é um diretório válido.")

    try:
        # Etapa 1️⃣ - Separar PDFs por tipo
        print("Processo 1")
        split_files = split_pdf_by_page(base_directory)

        # Etapa 2️⃣ - Extrair dados (valor, data, etc.)
        print("Processo 2")
        dados_extraidos = extract_pdf_data(base_directory)

        # Etapa 3️⃣ - Organizar nas past
        print("Processo 3")
        destino = organize_files_parallel(base_directory)

        # Contabiliza
        resultados["total_processado"] += 1
        if "nota" in destino.lower():
            resultados["notas_fiscais"].append(destino)
        elif "recibo" in destino.lower():
            resultados["recibos"].append(destino)
        else:
            resultados["outros"].append(destino)

    except Exception as e:
        resultados["erros"].append({"erro": str(e)})

    return resultados
