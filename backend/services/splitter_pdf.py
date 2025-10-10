from PyPDF2 import PdfReader, PdfWriter
from typing import List
import os

#nome da pasta que armazena os pfd's splitados
SPLIT_FOLDER_NAME = '__splits__'

# função para dividir os pdf's caso o pdf tenha varias paginas com varios arquivos
def split_pdf_by_page(file_path: str, output_base: str | None = None) -> List[str]:

    if output_base is None:
        dir_of_file = os.path.dirname(file_path)
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        output_base = os.path.join(dir_of_file, SPLIT_FOLDER_NAME, base_name)
    
    os.makedirs(output_base, exist_ok=True)

    reader = PdfReader(file_path)

    if getattr(reader, "is_encrypted", False):
        try:
            reader.decrypt("")
        except Exception:
            return []
        
    num_pages = len(reader.pages)

    if num_pages < 1:
        return [file_path]

    output_files = []

    for i in range(num_pages):
        writer = PdfWriter()
        writer.add_page(reader.pages[i])

        out_filename = f"{os.path.splitext(os.path.basename(file_path))}_page_{i+1}.pdf"
        out_path = os.path.join(output_base, out_filename)

    if not os.path.exists(out_path):
        with open(out_path, "wb") as f_out:
            writer.write(f_out)

    output_files.append(out_path)

    return output_files
       