# ─────────────────────────────────────────────────────────────────────────
# Winged Mind — imagem única que roda o backend Flask (que também serve
# todo o frontend estático: index.html, css/, js/, pages/, etc).
#
# Uso:
#   docker compose up --build
#   depois abra http://localhost:5001
# ─────────────────────────────────────────────────────────────────────────
FROM python:3.11-slim

# Dependências de sistema:
# - build-essential: compila pacotes sem wheel pronta pra arquitetura do host
#   (ex.: Macs Apple Silicon podem precisar compilar eventlet/gevent)
# - tesseract-ocr: motor de OCR usado pelo pytesseract (sem isso o OCR falha
#   silenciosamente em tempo de uso, mesmo com o import funcionando)
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Instala as dependências Python antes de copiar o resto do projeto —
# assim o Docker só reinstala pacotes quando requirements.txt muda,
# não a cada alteração de código.
COPY backend/requirements.txt backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copia o restante do projeto (backend + frontend estático na raiz)
COPY . .

WORKDIR /app/backend

EXPOSE 5001

CMD ["python", "run.py"]
