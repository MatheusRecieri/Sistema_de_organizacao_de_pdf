import os
import shutil
from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import Dict, List, Optional
from services.extractor_pdf import extract_pdf_data
from services.file_scanner import scan_directory
import time

#cria estrutura de pastas para organizar os arquivos e retorna dicionario com caminhos da pasta
def create_output_folders(base_path: str) -> dict:

    # organiza o nome das pastas
    folders = {
        "notas_fiscais": os.path.join(base_path, "notas_fiscais"),
        "recibos": os.path.join(base_path, "recibos"),
        "outros": os.path.join(base_path, "outros")
    }

    for folder_path in folders.values():
        os.makedirs(folder_path, exist_ok=True)
    #print(f"Pasta criada/verfificada: {folder_name} = { folder_path}")

    return folders

def process_single_file(args):
    """Processa um único arquivo - usado no multiprocessing"""
    pdf_file, base_path, folders = args
    
    try:
        data = extract_pdf_data(pdf_file)
        type_document = data.get("tipo", "")
        
        if type_document and "Nota Fiscal" in type_document:
            destination_folder = folders["notas_fiscais"]
            category = "notas_fiscais"
        elif type_document and "Recibo" in type_document:
            destination_folder = folders["recibos"]
            category = "recibos"
        else:
            destination_folder = folders["outros"]
            category = "outros"
        
        # Nome único baseado no hash do arquivo para evitar conflitos
        file_hash = str(hash(pdf_file))[-8:]
        base_name = os.path.splitext(os.path.basename(pdf_file))[0]
        ext = os.path.splitext(pdf_file)[1]
        new_filename = f"{base_name}_{file_hash}{ext}"
        destination_file = os.path.join(destination_folder, new_filename)
        
        shutil.copy2(pdf_file, destination_file)
        
        return {"status": "success", "category": category, "file": pdf_file}
    
    except Exception as e:
        return {"status": "error", "file": pdf_file, "error": str(e)}
    
def organize_files_parallel(base_path: str, max_workers: Optional[int] = None, cpu_mode: bool = True)-> Dict[str, int]:

    # print("Criando estrutura de pastas...")
    folders = create_output_folders(base_path)

    # print("Escanenadno diretorio...")
    pdf_files = scan_directory(base_path)
    # print(f"Encontrados {len(pdf_files)} arquivos PDF")

    if max_workers is None:
        max_workers = min(32, (os.cpu_count() or 1) * 4)

    stats = {
        "notas_fiscais": 0,
        "recibos": 0,
        "outros": 0,
        "erros": 0
    }

    # print(f"⚡ Processando {len(pdf_files)} arquivos com {max_workers} workers...")
    start_time = time.time()
    
    # Prepara argumentos para multiprocessing
    process_args = [(pdf_file, base_path, folders) for pdf_file in pdf_files]
    
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(process_single_file, args) for args in process_args]
        
        for i, future in enumerate(as_completed(futures), 1):
            try:
                result = future.result()
                
                # if result["status"] == "success":
                #     stats[result["category"]] += 1
                #     if i % 100 == 0 or i == len(pdf_files):
                #         print(f"📊 Progresso: {i}/{len(pdf_files)} - "
                #               f"NF: {stats['notas_fiscais']} | "
                #               f"Recibos: {stats['recibos']} | "
                #               f"Outros: {stats['outros']} | "
                #               f"Erros: {stats['erros']}")
                # else:
                #     stats["erros"] += 1
                    
            except Exception as e:
                stats["erros"] += 1
                print(f"❌ Erro no processamento: {str(e)}")
    
    elapsed_time = time.time() - start_time
    print(f"⏰ Tempo total: {elapsed_time:.2f} segundos")
    print(f"📊 Arquivos por segundo: {len(pdf_files) / elapsed_time:.2f}")
    
    return stats