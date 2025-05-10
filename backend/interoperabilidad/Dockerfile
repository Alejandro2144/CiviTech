# ─── Base image ─────────────────────────────────────────────────────────
FROM python:3.11-slim

# ─── Directorio de trabajo ─────────────────────────────────────────────
WORKDIR /app
ENV PYTHONUNBUFFERED=1

# ─── Instalación de dependencias ───────────────────────────────────────
COPY requirements.txt .
RUN pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# ─── Código de la aplicación ───────────────────────────────────────────
COPY . .

# ─── Puerto configurable ────────────────────────────────────────────────
ARG PORT=8003       # 📌 Cámbialo aquí si Interoperabilidad usa otro puerto
ENV PORT=${PORT}
EXPOSE ${PORT}

# ─── URLs de otros servicios ────────────────────────────────────────────
# 📌 Ajusta si cambias puertos o hosts
ENV CITIZEN_MS_URL=http://localhost:8001
ENV AUTH_MS_URL=http://localhost:8000
ENV DOCUMENT_MS_URL=http://localhost:8002

# ─── Variables externas ────────────────────────────────────────────────
ENV RABBIT_URL=amqp://localhost
ENV MINIO_ENDPOINT=http://localhost:9000

# ─── Inicio de la aplicación ───────────────────────────────────────────
ENTRYPOINT ["sh","-c"]
CMD ["uvicorn main:app --host 0.0.0.0 --port $PORT"]
