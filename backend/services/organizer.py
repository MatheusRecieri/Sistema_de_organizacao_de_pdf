import os
import shutil
from typing import Dict
from services.extractor_pdf import extract_pdf_data
from services.file_scanner import scan_directory

#cria estrutura de pastas para organizar os arquivos e retorna dicionario com caminhos da pasta
def create_output_folders(base_path: str) -> dict:

    # organiza o nome das pastas
    folders = {
        "arqivos_originais": os.path.join(base_path, "arquivos_originais"),
        "notas_fiscais": os.path.join(base_path, "notas_fiscais"),
        "recibos": os.path.join(base_path, "recibos"),
        "outros": os.path.join(base_path, "outros")
    }

    for folder_name, folder_path in folders.items():
        os.makedirs(folder_path, exist_ok=True)
    print(f"Pasta criada/verfificada: {folder_name} = { folder_path}")

    return folders

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
        "outros": 0,
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
                destination_folder = folders["outros"]
                stats["outros"]

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
                shutil.move(pdf_file, destination_file)
                print(f"   ✅ Copiado para: {data.get('tipo', 'Outros')}")
            else:
                shutil.move(pdf_file, destination_file)
                print(f"   ✅ Movido para: {data.get('tipo', 'Outros')}")

        except Exception as e:
            print(f"   ❌ Erro: {str(e)}")
            stats["erros"] += 1

    return stats