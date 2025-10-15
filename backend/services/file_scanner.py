# scaneia diretorios e cooderna o processaemntos deles

import os
import shutil
from typing import List, Dict
from services.extractor_pdf import extract_pdf_data
from services.splitter_pdf import split_pdf_by_page

PDF_EXTS = {".pdf"}
SPLIT_FOLDER_NAME = "split_pages"  #caminho das pastas

# varre um diretorio e todas as subpastas  proucurando arquivos PDF retorna lista de caminhos dos aruivos
def scan_directory(base_path: str) -> List[str]:
    
    results = []  # guarda o caminho completo dos arquivos
    
    # percorre todas as pastas e subpastas a partir do base_path
    # root camniho atual da pasta
    # dirs lista de subpastas
    # files lista de arquivos dentro de root
    for root, dirs, files in os.walk(base_path):

        if SPLIT_FOLDER_NAME in root or "split_by_type" in root:
            continue

        for fname in files:
            ext = os.path.splitext(fname)[1].lower()
            if ext in PDF_EXTS:
                full_path = os.path.join(root, fname)
                results.append(os.path.join(root,fname))

    return results

# Escaneia o diretório e prepara os PDFs por tipo de documentos, ignorando as pastas ja processadas, retorna uma lista de PDF separados por tipo
# def scan_and_split_by_type(base_path: str) -> List[str]:

#     # folders = create_output_folders(base_path)
#     prepareted_files = []

#     for root, dirs, files in os.walk(base_path):
        
#         # Ignora pastas já processadas
#         if any(skip in root for skip in [SPLIT_FOLDER_NAME, "split_by_type", "notas_fiscais", "recibos", "outros"]):
#             continue
            
#         for fname in files:
#             ext = os.path.splitext(fname)[1].lower()

#             if ext not in PDF_EXTS:
#                 continue

#             full_path = os.path.join(root, fname)

#             try:
#                 split_results = split_pdf_by_type(full_path)

#                 if split_results:
#                     prepareted_files.extend(split_results)
#                 else:
#                     prepareted_files.append(full_path)

#             except Exception as e:
#                 print(f"Erro ao separar por tipo {full_path}: {str(e)}")
#                 prepareted_files.append(full_path)

#     print(prepareted_files)
#     return prepareted_files

# # escaneia o diretorio e separa cada pdf página por página
# def scan_and_split(base_path:str, split_pages:bool = True) -> List[str]:
    
#     prepared_files = []

#     for root, dirs, files in os.walk(base_path):
#         if SPLIT_FOLDER_NAME in root:
#             continue

#         for fname in files:
#             ext = os.path.splitext(fname)[1].lower()

#         if ext in PDF_EXTS:
#             full_path = os.path.join(root, fname) 

#             if not split_pages:
#                 prepared_files.append(full_path)
#                 continue

#             try:
#                 split_results = split_pdf_by_page(full_path)

#                 if split_results:
#                     prepared_files.extend(split_results)
#                 else:
#                     prepared_files.extend(full_path)

#             except Exception as e:
#                 print(f"⚠️ Erro ao processar {full_path}: {str(e)}")
#                 prepared_files.append(full_path)

#     return prepared_files
    