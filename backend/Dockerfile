# ==========================================
# Stage 1: Build dependencies
# ==========================================
FROM python:3.11-slim AS builder

WORKDIR /app

# Install minimal OS dependencies for building binary wheels if required
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# ==========================================
# Stage 2: Production runtime image
# ==========================================
FROM python:3.11-slim AS runner

WORKDIR /app

# Copy installed Python dependencies from builder stage
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Copy application source
COPY backend /app/backend

# Configure dynamic port binding (Render/Cloud Run inject $PORT)
ENV PORT=8000
EXPOSE 8000

CMD ["sh", "-c", "uvicorn backend.app.main:app --host 0.0.0.0 --port ${PORT}"]