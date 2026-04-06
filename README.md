# AI Knowledge Base API

A backend service that provides a RESTful API for storing, searching, and querying user content (notes, articles, ideas) and augmenting them with local AI features such as embeddings and local LLM answers (via Ollama).


<div align="center">
  <h3>Video Demo (With text comments in Portuguese):</h3>
  <video src="https://github.com/user-attachments/assets/7b202273-4bc5-4a5f-af6c-b3ae38de1479" width="640" controls >
    Seu navegador não suporta vídeo.
  </video>
</div>

This project demonstrates backend fundamentals with an applied AI layer:

- Layered architecture (controllers, services, repositories) following the MVC pattern
- Request validation with Pydantic
- PostgreSQL persistence (configurable via the `DATABASE_URL` environment variable; async driver support)
- JWT authentication and password hashing
- Unit tests for functions of all layers and the API
- AI integration for embeddings and semantic search

## Prerequisites

- [Docker](https://www.docker.com/products/docker-desktop) and Docker Compose
- Or Python 3.11+ for local development without Docker

## Stack

- Python
- FastAPI
- Pydantic
- PostgreSQL
- Uvicorn
- Pytest
- Docker

## AI Stack

- Embeddings via `nomic-embed-text` (Ollama) for semantic search
- Cosine similarity search implemented in Python
- `Ollama` + `phi3:mini` for local LLM generation and QA

## Key Dependencies

- `fastapi` — web framework
- `uvicorn` — ASGI server
- `pydantic` — request/response validation
- `bcrypt` — password hashing
- `jose` — JWT tokens
- `httpx` — asynchronous requests for Ollama/embedding integration

## Project Structure

- `run.py` — local run entrypoint
- `app/server/server.py` — FastAPI application factory
- `app/controllers/` — route definitions and routers: `user_controller.py`, `note_controller.py`, `ai_controller.py`, `auth_controller.py`
- `app/services/` — business logic for users, notes and AI
- `app/repositories/` — persistence layer for users and notes
- `app/models/` — domain models
- `app/schemas/` — Pydantic schemas for requests/responses
- `app/database/` — database setup and helpers — supports PostgreSQL via `DATABASE_URL` and `asyncpg`
- `app/core/` — auth & security helpers
- `app/ai_settings/` — AI integration clients and helpers (Ollama client, embedding client)
- `api_tests/` and `app/services/*_test.py` — automated tests

## Installation

### Option 1 — Using Docker

Docker will set up the API, PostgreSQL, and Ollama automatically.

1. Clone the repository

```
git clone https://github.com/kevincontri/AI-Knowledge-Base-API.git
cd AI-Knowledge-Base-API
```

2. Start all services

```
docker compose up --build
```

This will:

- Build and start the API on `http://localhost:8000`
- Start a PostgreSQL instance with persistent storage
- Start an Ollama instance on `http://localhost:11434`

3. Pull the required models (first time only)

Open a new terminal and run:

```
docker exec -it ai_knowledge_base_api-ollama-1 ollama pull phi3:mini
docker exec -it ai_knowledge_base_api-ollama-1 ollama pull nomic-embed-text
```

4. Open the interactive docs at `http://localhost:8000/docs`

5. Start the app:

```
docker compose up
```
---

### Option 2 — Local development (without Docker)

1. Clone the repository

```
git clone https://github.com/kevincontri/AI-Knowledge-Base-API.git
cd AI-Knowledge-Base-API
```

2. Create and activate a virtual environment
   
```
python -m venv venv
venv\Scripts\Activate.ps1
```

3. Install dependencies

```
pip install -r requirements.txt
```

4. Configure the database connection

Set the `DATABASE_URL` environment variable to point at your PostgreSQL instance:

```
$env:DATABASE_URL = "postgresql://user:password@localhost:5432/ai_knowledge_db"
```

5. Install Ollama and pull the required models

Follow the [official Ollama installation](https://ollama.com) for your OS, then run:

```
ollama pull phi3:mini
ollama pull nomic-embed-text
```

6. Start the server

```
python run.py
```

Open the interactive docs at `http://127.0.0.1:8000/docs`

## Authentication

Authentication uses JWT bearer tokens and hashed passwords. Typical flow:

- Register a user via the users route
- Login with credentials to receive an `access_token`
- Include the token in requests as `Authorization: Bearer <token>` for protected endpoints

The project contains `app/core/auth.py` and `app/core/security.py` for token creation and credential verification.

## API Highlights

Routes are organized in `app/controllers/`:

- **Users** — list users
- **Auth** — register user and login to receive JWT tokens
- **Notes** — create, read, update, and delete personal notes associated with an author (by it's user id)
- **AI Endpoints** — semantic search using embeddings and cosine similarity; prompt enhancement and local LLM answering via Ollama

## Tests

```
pytest -q
```

## Future Improvements

- Add refresh tokens
- Expand AI features
- Deploy to cloud
