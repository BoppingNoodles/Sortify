
# ==========================================
# Stage 1: Build dependencies
# ==========================================
FROM python:3.11-slim AS builder

WORKDIR /app

# gcc covers any dependency that has to compile from source; it stays in the
# builder stage only. (No PostgreSQL client is used, so no libpq-dev.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Runtime dependencies only; dev, test and ML tooling stays out of the image.
COPY backend/requirements.txt requirements.txt

# Render has no GPU, so install the CPU-only torch build first. The default
# PyPI wheels bundle ~5 GB of CUDA libraries the service can never use.
# Only torch/torchvision come from the PyTorch index; everything else,
# including the already-satisfied torch lines, resolves from PyPI.
ARG TORCH_INDEX_URL=https://download.pytorch.org/whl/cpu
RUN pip install --no-cache-dir --user --index-url ${TORCH_INDEX_URL} torch torchvision \
    && pip install --no-cache-dir --user -r requirements.txt

# ==========================================
# Stage 2: Production runtime image
# ==========================================
FROM python:3.11-slim AS runner

WORKDIR /app

COPY --from=builder /root/.local /root/.local

ENV PATH=/root/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

COPY backend /app/backend

ENV PORT=8000
EXPOSE 8000

CMD ["sh", "-c", "uvicorn backend.app.main:app --host 0.0.0.0 --port ${PORT}"]
