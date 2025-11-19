# Arquivo reponsável por extrair informações do pdf

import pdfplumber
import os
import re
from typing import Dict, List, Optional
import hashlib
from functools import lru_cache


@lru_cache(maxsize=1000)
def get_file_signature(file_path: str) -> str:
    """Gera assinatura única do arquivo para cache"""
    stat = os.stat(file_path)
    return hashlib.md5(f"{file_path}{stat.st_size}{stat.st_mtime}".encode()).hexdigest()


# lê o pdf e extrai informações importantes
def extract_pdf_data(file_path: str) -> Dict[str, Optional[str]]:
    try:

        cache_key = get_file_signature(file_path)

        # abre o pdf
        with pdfplumber.open(file_path) as pdf:
            text = ""

            for page in pdf.pages[:3]:
                text = page.extract_text()
                if text:
                    text += text + "\n"

                # para early return se já identificou o tipo
                if "recibo" in text.lower() and "nota fiscal" in text.lower():
                    break
            # doc_type = "outros"
            # value = None
            # date = None
        text_lower = text.lower()
        doc_type = "outros"

        if any(keyword in text_lower for keyword in ["nota fiscal", "nfs-e", "nf-e"]):
            doc_type = "Nota Fiscal"
        elif any(
            keyword in text_lower for keyword in ["recibo", "comprovante", "pagamento"]
        ):
            doc_type = "Recibo"

        return {"arquivo": file_path, "tipo": doc_type}

    except Exception as e:
        return {"arquivo": file_path, "tipo": "Erro", "erro": str(e)}
