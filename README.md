# AI Knowledge Base API

A backend service that provides a RESTful API for storing, searching, and querying user content (notes, articles, ideas) and augmenting them with local AI features such as embeddings and local LLM answers (via Ollama).

This project demonstrates backend fundamentals with an applied AI layer:

- Layered architecture (controllers, services, repositories)
- Request validation with Pydantic
- PostgreSQL persistence (configurable via the `DATABASE_URL` environment variable; async driver support)
- JWT authentication and password hashing
- AI integration for embeddings and prompt enhancement

## Stack

- Python
- FastAPI
- Pydantic
- PostgreSQL
- Uvicorn

## AI Stack

The project includes an AI stack for semantic search and local LLM answers:

- `pgvector` + Embeddings (with external provider)
- `Ollama` (local LLM for generation / QA)

## Key Dependencies

- `fastapi` — web framework
- `uvicorn` — ASGI server
- `pydantic` — request/response validation
- `bcrypt` — password hashing
- `jose` — JWT tokens
- `httpx` — Asynchronous requests for Ollama/embedding integration.

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

1. Clone the repository

```
git clone <repo-url>
cd AI-Knowledge-Base-API
```

2. Create and activate a virtual environment

Windows (PowerShell):

```
python -m venv venv
venv\Scripts\Activate.ps1
```

3. Install dependencies

```
pip install -r requirements.txt
```

4. Configure the database connection

Set the `DATABASE_URL` environment variable to point at your PostgreSQL instance. Example (PowerShell):

```
$env:DATABASE_URL = "postgresql://user:password@localhost:5432/ai_knowledge_db"
```

The application will automatically use `asyncpg` for PostgreSQL when the URL scheme is `postgresql://` or `postgres://`.

## Run the server (local development)

The project includes a simple runner. Start the server with:

```
python run.py
```

This runs `uvicorn` targeting `app.server.server:app` with reload enabled (default host `127.0.0.1:8000`).

Open the interactive docs at:

```
http://127.0.0.1:8000/docs
```

## Authentication

Authentication uses JWT bearer tokens and hashed passwords. Typical flow:

- Register a user (via the users route)
- Login with credentials to receive an `access_token`
- Include the token in requests as `Authorization: Bearer <token>` for protected endpoints

The project contains `app/core/auth.py` and `app/core/security.py` for token creation and credential verification.

## API Highlights

Note: Routes are organized in `app/controllers/`. High-level capabilities:

- Users
  - Register and list users
- Auth
  - Login to receive JWT tokens
- Notes (content)
  - Create, read, update, delete personal notes
  - Notes are associated with an author (user)
- AI Endpoints
  - Embeddings and semantic search using the `embedding_client` in `app/ai_settings`
  - Prompt enhancement and local LLM answering via the `ollama_client` and `prompt_enhancer`

Refer to the controller files for concrete route paths and request shapes.

## Ollama installation (local LLM)

This project can use Ollama as a local LLM for generation and question-answering. Below are concise installation and quick-start instructions.

1. Install Ollama

- macOS (Homebrew):

```
brew install ollama
```

- Linux: follow the official installer or use the distro package if available; you can also run Ollama in Docker. See the official docs for the recommended installer for your distribution.

- Windows: use WSL (Windows Subsystem for Linux) and follow the Linux instructions, or use the Ollama Desktop if available for Windows. See the official docs.

2. Verify installation

```
ollama --version
```

3. Pull phi3:mini model (The one used in this project)

```
ollama pull phi3:mini
```

4. Run the model locally (quick test)

```
ollama run phi3:mini --prompt "Hello, Ollama"
```

- Now Ollama is running in your machine.

## Tests

There are unit tests under `api_tests/` and `app/services/*_test.py`. Run tests with your preferred test runner (e.g., `pytest`).

```
pytest -q
```

## Future Improvements

- Add refresh tokens and improved session handling
- Expand AI features: vector DB support, advanced retrieval-augmented generation
