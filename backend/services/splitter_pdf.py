# divide o pdf original em varios outros pdfs, identifica se no pdf original tem mais de uma nota 
import fitz  
import os
from concurrent.futures import ProcessPoolExecutor
from typing import List

# Divide as paginas do pdf em arquivos pdf individuais
def split_pdf_by_page(file_path) -> List[str]:
    """
    Separa cada página do PDF em arquivo individual.
    """
    try:

        doc = fitz.open(file_path)

        # verifica se o doc tem apenas uma página, se tiver vai sair do doc e ir para outro
        if len(doc) == 1:
            doc.close()
            return [file_path]
        
        base_dir = os.path.dirname(file_path)
        filename = os.path.splitext(os.path.basename(file_path))[0]
        split_folder = os.path.join(base_dir, "split_pages", filename)
        os.makedirs(split_folder, exist_ok=True)

        output_files = []

        for page_num in range(len(doc)):
            new_pdf = fitz.open()
            new_pdf.insert_pdf(doc, from_page=page_num, to_page=page_num)

            output_filename = os.path.join(split_folder, f"{filename}_p{page_num + 1}.pdf")
            new_pdf.save(output_filename)
            new_pdf.close()
            output_files.append(output_filename)
        
        doc.close()
        return output_files
        
    except Exception as e:
        print(f"Erro ao separar PDF {file_path}? {str(e)}")
        return [file_path]

# processa splitting em lotes com paralelização
def batch_split_pdfs(pdf_files: List[str], batch_size: int = 50) -> List[str]:

    all_results = []

    for i in range(0, len(pdf_files), batch_size):
        batch = pdf_files[i:i + batch_size]
        print(f"Processando lote: {i//batch_size + 1}/{(len(pdf_files)-1)//batch_size + 1}")

        with ProcessPoolExecutor(max_workers=8) as executor:
            batch_results = list(executor.map(split_pdf_by_page, batch))

        for result in batch_results:
            if result:
                all_results.extend(result)

    return all_results           
