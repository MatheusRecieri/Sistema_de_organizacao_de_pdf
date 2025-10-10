import pdfplumber
import re

def extract_pdf_data(file_path: str) -> dict:
    try:
        with pdfplumber.open(file_path) as pdf:
            text = ""

            for page in pdf.pages:
                text += page.extract_text() or ""

            if "recibo" in text.lower().strip():
                doc_type = "Recibo de locação"
            elif "nota fiscal" in text.lower():
                doc_type = "Nota Fiscal"
            else:
                doc_type = "Desconhecido"

            valor = None
            match_valor = re.search(r"(\d{1,3}(?:\.\d{3})*,\d{2})", text)

        if match_valor:
            valor = match_valor.group(1)

            data = None
        match_data = re.search(r"(\d{2}/\d{2}/\d{4})", text)
        if match_data:
            data = match_data.group(1)

        return {
            "arquivo": file_path,
            "tipo": doc_type,
            "valor": valor,
            "data": data
        }
    except Exception as e :
        return {"arquivo": file_path, "erro": str(e)}