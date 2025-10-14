# divide o pdf original em varios outros pdfs, identifica se no pdf original tem mais de uma nota 
import fitz  
import os
from concurrent.futures import ThreadPoolExecutor

# Divide as paginas do pdf em arquivos pdf individuais
def split_pdf_by_page(file_path):
    """
    Separa cada página do PDF em arquivo individual.
    """
    try:
        base_dir = os.path.dirname(file_path)
        filename = os.path.splitext(os.path.basename(file_path))[0]
        split_folder = os.path.join(base_dir, "split_pages", filename)

        os.makedirs(split_folder, exist_ok=True)

        doc = fitz.open(file_path)
        output_files = []

        for page_num in range(len(doc)):
            # Cria um novo pdf para cada página
            new_pdf = fitz.open()
            new_pdf.insert_pdf(doc, from_page=page_num, to_page=page_num)

            # Salva em um novo pdf (CORRIGIDO: adicionado número da página)
            output_filename = os.path.join(split_folder, f"{filename}_page_{page_num + 1}.pdf")
            new_pdf.save(output_filename)
            new_pdf.close()

            output_files.append(output_filename)

        doc.close()
        return output_files
    
    except Exception as e:
        print(f"Erro ao separar PDF {file_path}: {str(e)}")
        return []

# separa as paginas do pdf agrupando por tipo de documento 
def split_pdf_by_type(file_path):
    """
    Lê um PDF e separa os documentos internos com base em palavras-chave.
    Identifica notas fiscais e recibos de locação.
    """
    try:
        doc = fitz.open(file_path)

        # Variáveis de controle
        base_dir = os.path.dirname(file_path)
        filename = os.path.splitext(os.path.basename(file_path))[0]
        split_folder = os.path.join(base_dir, "split_by_type")

        os.makedirs(split_folder, exist_ok=True)

        output_files = []
        current_writer = None
        current_doc_index = 1
        current_type = None

        # Palavras-chave que identificam tipos de documentos
        keywords: dict[str, list[str]] = {
            "nota": ["Nota Fiscal de Serviço", "NFS-e", "Prestação de Serviços", "NOTA FISCAL", "Nota Fiscal", "nota fiscal"],
            "recibo": ["Recibo de Locação", "Recibo de Pagamento", "Recibo", "RECIBO"]
        }

        # Percorrer todas as páginas do PDF
        for page_index in range(len(doc)):
            page = doc.load_page(page_index)
            text = page.get_text("text")

            # Verificar se a página contém uma das palavras-chave
            found_type = None
            for tipo, palavras in keywords.items():
                # CORRIGIDO: iterar sobre cada palavra da lista
                for palavra in palavras:
                    if palavra.lower() in text.lower(): # pyright: ignore[reportAttributeAccessIssue]
                        found_type = tipo
                        break
                if found_type:
                    break

            if not found_type:
                found_type = "outros"

            # Se mudou o tipo de documento
            if current_type != found_type:
                # Salvar documento anterior se existir
                if current_writer is not None and current_writer.page_count > 0:
                    output_filename = os.path.join(
                        split_folder,
                        f"{filename}_{current_type}_{current_doc_index}.pdf"
                    )
                    current_writer.save(output_filename)
                    output_files.append(output_filename)
                    current_writer.close()
                    current_doc_index += 1  # CORRIGIDO: estava "current_doc_inde"
                
                # Iniciar novo documento
                current_writer = fitz.open()
                current_type = found_type

            # CORRIGIDO: garantir que current_writer existe antes de usar
            if current_writer is not None:
                current_writer.insert_pdf(doc, from_page=page_index, to_page=page_index)
            
        # Salvar o último documento se ainda tiver conteúdo
        if current_writer is not None and current_writer.page_count > 0:
            output_filename = os.path.join(
                split_folder,
                f"{filename}_{current_type}_{current_doc_index}.pdf"
            )
            current_writer.save(output_filename)
            output_files.append(output_filename)
            current_writer.close()

        doc.close()
        return output_files
        
    except Exception as e:
        print(f"Erro ao separar PDF por tipo {file_path}: {str(e)}")
        return []

def parallel_split_pdfs(pdf_files):
    with ThreadPoolExecutor(max_workers=8) as executor:
        results = list(executor.map(split_pdf_by_type, pdf_files))
    flattened = [f for sublist in results for f in sublist if sublist]
    return flattened