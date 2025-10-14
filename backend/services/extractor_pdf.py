# Arquivo reponsável por extrair informações do pdf

import pdfplumber
import re
from typing import Dict, List, Optional
from concurrent.futures import ThreadPoolExecutor,  as_completed # bibloteca para manipular os threads do cpu
import multiprocessing
import queue
import threading

# lê o pdf e extrai informações importantes
def extract_pdf_data(file_path: str) -> Dict[str, Optional[str]]:
    try:

        REGEX_VALUE = re.compile(r'(\d{1,3}(?:\.\d{3})*,\d{2})')
        REGEX_DATE = re.compile(r'(\d{2}/\d{2}/\d{4})')

        #abre o pdf
        with pdfplumber.open(file_path) as pdf:
            text = ""
            doc_type = "outros"
            value = None
            date = None

            # leitrua inteligente, logo nas primeiras páginas
            max_pages = min(3, len(pdf.pages))

            for page_num in range(max_pages):
                page_text = pdf.pages[page_num].extract_text() or ""
                text += page_text

                if doc_type == "outros" and page_num == 0:
                    text_lower = page_text.lower()

                    if "recibo" in text_lower:
                        doc_type = "Recibo de locação"
                    elif "nota fiscal" in text_lower or "nfs-e" in text_lower:
                        doc_type = "Nota Fiscal"

                if not value:
                    match_value = REGEX_VALUE.search(page_text)

                    if match_value:
                        value = match_value.group(1) 

                if not date:
                    match_date = REGEX_DATE.search(page_text)    

                    if match_date:
                        date = match_date.group(1)

                if doc_type != "outros" and value and date:
                    break

        # Retorda dados
        return {
            "arquivo": file_path,
            "tipo": doc_type,
            "valor": value,
            "data": date
        }
    except Exception as e :
        return {"arquivo": file_path, "tipo": "Erro", "erro": str(e)}

# Processa PDFs em listas
class PDFProcessingQueue:
    """
    Classe que processa PDFs em fila com múltiplas threads.
    Ideal para servidor: leve, escalável e controlável.
    """
    def __init__(self, max_workers: int = 2):
        self.max_workers = max_workers
        self.work_queue = queue.Queue()
        self.results = []
        self.is_running = False
        self.total_files = 0
        self.processed_files = 0
        self._lock = threading.Lock()

    def add_files(self, file_paths: List[str]):
        """Adiciona arquivos à fila."""
        self.total_files = len(file_paths)
        for file_path in file_paths:
            self.work_queue.put(file_path)

    def _worker(self):
        """Thread que processa os arquivos da fila."""
        while self.is_running:
            try:
                file_path = self.work_queue.get(timeout=1)
                result = extract_pdf_data(file_path)

                with self._lock:
                    self.results.append(result)
                    self.processed_files += 1

                self.work_queue.task_done()

            except queue.Empty:
                continue
            except Exception as e:
                print(f"Erro no worker: {e}")

    def start(self):
        """Inicia o processamento da fila."""
        self.is_running = True
        self.processed_files = 0
        self.results = []

        workers = []
        for _ in range(self.max_workers):
            worker = threading.Thread(target=self._worker, daemon=True)
            worker.start()
            workers.append(worker)

        self.work_queue.join()

        self.is_running = False
        for worker in workers:
            worker.join(timeout=2)

    def get_results(self) -> List[Dict]:
        """Retorna todos os resultados."""
        return self.results

    def get_progress(self) -> tuple:
        """Retorna o progresso (processados, total)."""
        return (self.processed_files, self.total_files)


# ========================================================================
# FUNÇÃO DE USO EXTERNO
# ========================================================================
def extract_pdf_data_server_safe(file_paths: List[str], max_workers: int = 2):
    """
    Função segura e recomendada para o servidor.
    Usa a fila interna de processamento.
    """
    queue_processor = PDFProcessingQueue(max_workers=max_workers)
    queue_processor.add_files(file_paths)
    queue_processor.start()
    return queue_processor.get_results()