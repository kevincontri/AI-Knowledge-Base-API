import httpx
import os
import dotenv

dotenv.load_dotenv()

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")

class OllamaClient:

    def __init__(self, base_url: str = OLLAMA_URL):
        self.endpoint = f"{base_url}/api/chat"

    async def generate(self, prompt: str):
        payload = {
            "model": "phi3:mini",
            "stream": False,
            "messages": [{"role": "user", "content": prompt}],
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(self.endpoint, json=payload)
            response.raise_for_status()
            return response.json()
