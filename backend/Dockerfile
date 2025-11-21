FROM python:3.11-slim

# Diretório de trabalho
WORKDIR /app

# Instala dependências necessárias
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpoppler-cpp-dev \
    tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

# Copia os arquivos de requisitos
COPY requirements.txt .

# Instala dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do backend
COPY . .

# Porta que o app expõe
EXPOSE 5000

# Comando para iniciar o FastAPI com Uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
