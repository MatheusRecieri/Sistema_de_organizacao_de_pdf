import fitz  # PyMuPDF
import os

def split_pdf_by_type(file_path):
    """
    Lê um PDF e separa os documentos internos com base em palavras-chave.
    Identifica notas fiscais e recibos de locação.
    """

    # Abrir o PDF original
    doc = fitz.open(file_path)

    # Variáveis de controle
    output_files = []
    current_writer = fitz.open()
    current_doc_index = 1
    current_type = "desconhecido"

    # Palavras-chave que identificam tipos de documentos
    keywords = {
        "nota": ["Nota Fiscal de Serviço", "NFS-e", "Prestação de Serviços"],
        "recibo": ["Recibo de Locação", "Recibo de Pagamento", "Recibo"]
    }

    # Percorrer todas as páginas do PDF
    for page_index in range(len(doc)):
        page = doc.load_page(page_index)
        text = page.get_text("text")

        # Verificar se a página contém uma das palavras-chave
        found_type = None
        for tipo, palavras in keywords.items():
            if any(palavra.lower() in text.lower() for palavra in palavras):
                found_type = tipo
                break

        # Se achou um novo tipo e já temos páginas acumuladas, salvar o documento anterior
        if found_type and current_writer.page_count > 0:
            output_filename = f"{os.path.splitext(file_path)[0]}_{current_type}_{current_doc_index}.pdf"
            current_writer.save(output_filename)
            output_files.append(output_filename)
            current_writer.close()

            # Preparar o próximo documento
            current_writer = fitz.open()
            current_doc_index += 1
            current_type = found_type

        # Se ainda não temos um tipo, assume o atual (pode ser o primeiro documento)
        if found_type and current_type == "desconhecido":
            current_type = found_type

        # Adiciona a página atual no PDF em montagem
        current_writer.insert_pdf(doc, from_page=page_index, to_page=page_index)

    # Salvar o último documento se ainda tiver conteúdo
    if current_writer.page_count > 0:
        output_filename = f"{os.path.splitext(file_path)[0]}_{current_type}_{current_doc_index}.pdf"
        current_writer.save(output_filename)
        output_files.append(output_filename)
        current_writer.close()

    return output_files
