import os
from typing import List
from services.splitter_pdf import split_pdf_by_type

PDF_EXTS = {".pdf"}
# XML_EXTS = {".xml"}


# recebe um string base_path que é o caminho inicial (entrada de dados do front end)
def scan_directory(base_path: str) -> List[str]:
    results = []  # guarda o caminho completo dos arquivos
    
    # percorre todas as pastas e subpastas a partir do base_path
    # root camniho atual da pasta
    # dirs lista de subpastas
    # files lista de arquivos dentro de root
    for root, dirs, files in os.walk(base_path):

        if SPLIT_FOLDER_NAME in root:
            continue
        for fname in files:
            ext = os.path.splitext(fname)[1].lower()
            if ext in PDF_EXTS:
                results.append(os.path.join(root,fname))
    return results


def scan_and_split(base_path:str, split_pages:bool = True) -> List[str]:
    
    prepared_files = []

    for root, dirs, files in os.walk(base_path):
        if SPLIT_FOLDER_NAME in root:
            continue

        for fname in files:
            ext = os.path.splitext(fname)[1].lower()
            full_path = os.path.join(root, fname) 

        if ext in PDF_EXTS:
            if not split_pages:
                prepared_files.append(full_path)
                continue

            try:
                split_results = split_pdf_by_page(full_path)

                if split_results:
                    prepared_files.extend(split_results)
                else:
                    prepared_files.extend(full_path)
            except Exception:
                prepared_files.append(full_path)

    return prepared_files