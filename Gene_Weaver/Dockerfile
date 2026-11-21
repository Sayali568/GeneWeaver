# Multi-stage production Dockerfile for GeneWeaver
# Stage 1: Build & Dependencies
FROM python:3.12-slim AS builder

WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Final Runtime
FROM python:3.12-slim AS runner

WORKDIR /app

# Create non-privileged user for security
RUN groupadd -g 1001 geneweaver && \
    useradd -u 1001 -g geneweaver -s /bin/bash -m geneweaver

# Copy python dependencies from builder
COPY --from=builder /root/.local /home/geneweaver/.local
ENV PATH=/home/geneweaver/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Copy application source code
COPY --chown=geneweaver:geneweaver . /app

USER geneweaver

# Expose FastAPI application port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/api/v1/health')" || exit 1

# Launch production ASGI server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
