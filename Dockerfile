# ── Build stage ─────────────────────────────────────────────────
FROM python:3.11-slim AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ── Production stage ────────────────────────────────────────────
FROM python:3.11-slim

WORKDIR /app

# Copiar dependencias del builder
COPY --from=builder /install /usr/local

# Copiar código de la aplicación
COPY app/ ./app/

# Crear usuario no-root por seguridad
RUN useradd --create-home appuser && chown -R appuser:appuser /app
USER appuser

# Exponer puerto
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Ejecutar la aplicación
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
