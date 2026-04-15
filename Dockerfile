# Stage 1: Builder - install dependencies into a virtual environment
FROM python:3.11-slim AS builder

WORKDIR /build

RUN python -m venv /build/venv

COPY requirements.txt .

RUN /build/venv/bin/pip install --no-cache-dir -r requirements.txt


# Stage 2: Runtime - minimal final image with non-root user
FROM python:3.11-slim AS runtime

# Create non-root group and user
RUN groupadd --gid 1001 appgroup && \
    useradd --uid 1001 --gid appgroup --no-create-home appuser

WORKDIR /app

# Copy only the installed dependencies from the builder stage
COPY --from=builder /build/venv /app/venv

# Copy application code and set ownership to non-root user
COPY --chown=appuser:appgroup . .

# Add venv binaries to PATH
ENV PATH="/app/venv/bin:$PATH"

# Switch to non-root user
USER appuser

CMD ["uvicorn", "app.server.server:app", "--host", "0.0.0.0", "--port", "8000"]
