import httpx


class EmbeddingClient:

    def __init__(self, base_url: str = "http://localhost:11434"):
        self.endpoint = f"{base_url}/api/embeddings"

    async def message_embedding(self, message: str) -> list[float]:
        payload = {"model": "nomic-embed-text", "prompt": message}

        async with httpx.AsyncClient(timeout=35.0) as client:
            response = await client.post(self.endpoint, json=payload)
            response.raise_for_status()
            data = response.json()
            return data["embedding"]
