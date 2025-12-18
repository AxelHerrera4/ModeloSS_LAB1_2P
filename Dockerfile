# Dockerfile para el Scanner de Vulnerabilidades con ML
# Imagen optimizada para ejecución en CI/CD

FROM python:3.11-slim

# Metadatos
LABEL maintainer="Security Team"
LABEL description="ML-based Vulnerability Scanner for Python and JavaScript"
LABEL version="1.0.0"

# Variables de entorno
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema (git para get_changed_files.py)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        git \
        && \
    rm -rf /var/lib/apt/lists/*

# Copiar requirements primero (para cachear la capa)
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código fuente
COPY ml_model/ ./ml_model/
COPY scripts/ ./scripts/
COPY config.yml .

# Crear directorio para reportes
RUN mkdir -p /app/reports

# Usuario no-root para seguridad
RUN useradd -m -u 1000 scanner && \
    chown -R scanner:scanner /app
USER scanner

# Healthcheck (verifica que el modelo existe)
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import os; exit(0 if os.path.exists('ml_model/vulnerability_detector.pkl') else 1)"

# Punto de entrada: Ejecutar la API Flask por defecto
ENTRYPOINT ["python", "api.py"]
