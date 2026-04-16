FROM python:3.11-slim AS builder

WORKDIR /app

RUN python -m venv /app/venv

COPY requirements.txt .

RUN /app/venv/bin/pip install --no-cache-dir -r requirements.txt


FROM python:3.11-slim AS runtime

RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/* && \
    groupadd --gid 1001 appgroup && \
    useradd --uid 1001 --gid appgroup --no-create-home appuser

WORKDIR /app

COPY --from=builder /app/venv /app/venv

COPY --chown=appuser:appgroup . .

ENV PATH="/app/venv/bin:$PATH"

USER appuser

CMD ["uvicorn", "app.server.server:app", "--host", "0.0.0.0", "--port", "8000"]