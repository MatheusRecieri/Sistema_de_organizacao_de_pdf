import os
from services.splitter_pdf import split_pdf_by_page
from services.extractor_pdf import extract_pdf_data
from services.organizer import organize_files_parallel

# def processar_pipeline(base_directory):

#     resultados = {
#         "total-processados": 0,
#         "notas-fiscais": [],
#         "recibos": [],
#         "outros": [],
#         "erros": [],
#     }

#     if not os.path.isdir(base_directory):
#         raise ValueError(f"O caminho {base_directory} não é um diretório válido.")

#     # Cria as pastas finais dentro do diretório base
#     nf_folder = os.path.join(base_directory, "NFEs")
#     recibos_folder = os.path.join(base_directory, "Recibos")
#     outros_folder = os.path.join(base_directory, "Outros")
#     os.makedirs(nf_folder, exist_ok=True)
#     os.makedirs(recibos_folder, exist_ok=True)
#     os.makedirs(outros_folder, exist_ok=True)

#     # Percorre o diretório inteiro
#     for root, _, files in os.walk(base_directory):
#         for file in files:
#             if file.lower().endswith(".pdf"):
#                 file_path = os.path.join(root, file)
#                 try:
#                     # Etapa 1️⃣ - Separar PDFs por tipo
#                     split_files = split_pdf_by_page(file_path)

#                     for split_file in split_files:
#                         # Etapa 2️⃣ - Extrair dados (valor, data, etc.)
#                         dados_extraidos = extract_pdf_data(split_file)

#                         # Etapa 3️⃣ - Organizar nas pastas
#                         destino = organize_files_parallel(base_directory)

#                         # Contabiliza
#                         resultados["total_processado"] += 1
#                         if "nota" in destino.lower():
#                             resultados["notas_fiscais"].append(destino)
#                         elif "recibo" in destino.lower():
#                             resultados["recibos"].append(destino)
#                         else:
#                             resultados["outros"].append(destino)

#                 except Exception as e:
#                     resultados["erros"].append({"arquivo": file, "erro": str(e)})

#     return resultados


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
