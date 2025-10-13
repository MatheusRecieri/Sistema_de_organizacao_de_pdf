# scaneia diretorios e cooderna o processaemntos deles

import os
import shutil
from typing import List, Dict
from services.extractor_pdf import extract_pdf_data
from services.splitter_pdf import split_pdf_by_page, split_pdf_by_type

PDF_EXTS = {".pdf"}
SPLIT_FOLDER_NAME = "split_pages"  #caminho das pastas

#cria estrutura de pastas para organizar os arquivos e retorna dicionario com caminhos da pasta
def create_output_folders(base_path: str) -> dict:

    # organiza o nome das pastas
    folders = {
        "arqivos_originais": os.path.join(base_path, "arquivos_originais"),
        "notas_fiscais": os.path.join(base_path, "notas_fiscais"),
        "recibos": os.path.join(base_path, "recibos")
    }

    for folder_name, folder_path in folders.items():
        os.makedirs(folder_path, exist_ok=True)
    print(f"Pasta criada/verfificada: {folder_name} = { folder_path}")

    return folders

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

# Escaneia o diretório e prepara os PDFs ppor tipo de documentos, ignorando as pastas ja processadas, retorna uma lista de PDF separados por tipo
def scan_and_split_by_type(base_path: str) -> List[str]:

    # folders = create_output_folders(base_path)
    prepareted_files = []

    for root, dirs, files in os.walk(base_path):
        
        # Ignora pastas já processadas
        if any(skip in root for skip in [SPLIT_FOLDER_NAME, "split_by_type", "arquivos_originais", "notas_fiscais", "recibos"]):
            continue
            
        for fname in files:
            ext = os.path.splitext(fname)[1].lower()

            if ext not in PDF_EXTS:
                continue

            full_path = os.path.join(root, fname)

            try:
                split_results = split_pdf_by_type(full_path)

                if split_results:
                    prepareted_files.extend(split_results)
                else:
                    prepareted_files.append(full_path)

            except Exception as e:
                print(f"Erro ao separar por tipo {full_path}: {str(e)}")
                prepareted_files.append(full_path)

    return prepareted_files

# escaneia o diretorio e separa cada pdf página por página
def scan_and_split(base_path:str, split_pages:bool = True) -> List[str]:
    
    prepared_files = []

    for root, dirs, files in os.walk(base_path):
        if SPLIT_FOLDER_NAME in root:
            continue

        for fname in files:
            ext = os.path.splitext(fname)[1].lower()

        if ext in PDF_EXTS:
            full_path = os.path.join(root, fname) 

            if not split_pages:
                prepared_files.append(full_path)
                continue

            try:
                split_results = split_pdf_by_page(full_path)

                if split_results:
                    prepared_files.extend(split_results)
                else:
                    prepared_files.extend(full_path)

            except Exception as e:
                print(f"⚠️ Erro ao processar {full_path}: {str(e)}")
                prepared_files.append(full_path)

    return prepared_files

# organiza os arquivos pdf em pastas por tipo de documentos
def organize_files(base_path: str, copy_mode: bool = True) -> Dict[str, int]:

    print("Criadno estrutura de páginas")
    folders = create_output_folders(base_path)

    print("Scaneando diretorio")
    pdf_files = scan_directory(base_path)
    print(f"Encontrados {len(pdf_files)}")

    stats = {
        "notas_fiscais": 0,
        "recibos": 0,
        "desconhecidos": 0,
        "erros": 0
    }

    #processar cada PDF
    print("Processamento de pdf")

    for i, pdf_file in enumerate(pdf_files, 1):
         print(f"[{i}/{len(pdf_files)}] Processando: {os.path.basename(pdf_file)}")
        
        try:
        
            data = extract_pdf_data(pdf_file)

            if "Nota Fiscal" in data.get("tipo", ""):
                destination_folder = folders["notas_fiscais"]
            elif "Recibo" in data.get("tipo", ""):
                destination_folder = folders["recibos"]
            else:
                destination_folder = folders["desconhecidos"]
                stats["desconhecidos"]

            # evita sobrescrever arquivo existente

            destination_file = os.path.join(destination_folder, os.path.basename(pdf_file))

            if os.path.exists(destination_file):
                # Adiciona nome ao arquivo pdf
                base_name = os.path.splitext(os.path.basename(pdf_file))[0]
                ext = os.path.splitext(os.path.basename(pdf_file))[1]
                counter = 1

                while os.path.exists(destination_file):
                    new_name = f"{base_name}_{counter}{ext}"
                    destination_file = os.path.join(destination_folder, new_name)
                    counter += 1
            # copia ou move o arquivo
            if copy_mode:
                shutil.copy2(pdf_file, destination_file)
                print(f"   ✅ Copiado para: {data.get('tipo', 'Desconhecido')}")
            else:
                shutil.move(pdf_file, destination_file)
                print(f"   ✅ Movido para: {data.get('tipo', 'Desconhecido')}")
        
        except Exception as e:
            print(f"   ❌ Erro: {str(e)}")
            stats["erros"] += 1
    