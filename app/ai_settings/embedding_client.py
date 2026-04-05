import httpx
import os
import dotenv

dotenv.load_dotenv()

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")


class EmbeddingClient:

    def __init__(self, base_url: str = OLLAMA_URL):
        self.endpoint = f"{base_url}/api/embed"

    async def message_embedding(self, message: str) -> list[float]:
        payload = {"model": "nomic-embed-text", "input": message}

        async with httpx.AsyncClient(timeout=35.0) as client:
            response = await client.post(self.endpoint, json=payload)
            response.raise_for_status()
            data = response.json()
            return data["embeddings"][0]
