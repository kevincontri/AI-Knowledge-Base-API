from app.repositories.interfaces.user_repository import UserRepositoryInterface
from app.repositories.interfaces.note_repository import NoteRepositoryInterface
from app.exceptions.exceptions import NotFoundError
from app.services.interfaces.ai_service import AIServiceInterface
from app.ai_settings.ollama_client import OllamaClient
from app.ai_settings.prompt_enhancer import PROMPT_ENHANCER
from app.schemas.ai_schemas import *
from app.ai_settings.embedding_client import EmbeddingClient
import math


class AIService(AIServiceInterface):

    def __init__(
        self, note_repo: NoteRepositoryInterface, user_repo: UserRepositoryInterface
    ):
        self.note_repo = note_repo
        self.user_repo = user_repo

    async def ask(self, user_id: int, prompt: str):
        user_notes = await self.__get_user_notes(user_id)

        ollama_client = OllamaClient()
        embed_client = EmbeddingClient()

        query = f"User question about notes: {prompt}"

        embeddings = await embed_client.message_embedding(query)
        ranked_notes = self.__semantic_search(embeddings, user_notes)
        clean_notes = self.__prepare_notes_for_llm(ranked_notes)

        enriched_prompt = PROMPT_ENHANCER.format(notes=clean_notes, user_prompt=prompt)

        response = await ollama_client.generate(enriched_prompt)
        llm_response = response["message"]["content"]

        return PromptResponse(ai_response=llm_response)

    async def __get_user_notes(self, user_id: int):
        if await self.user_repo.get_user_by_id(user_id):
            notes = await self.note_repo.get_user_notes(user_id=user_id)
            return notes
        else:
            raise NotFoundError("User not found")

    # Cosine similarity, it measures how similar two vectors are
    def __cosine_similarity(self, vector1, vector2):
        dot_product = sum(a * b for a, b in zip(vector1, vector2))
        magnitude1 = math.sqrt(sum(a**2 for a in vector1))
        magnitude2 = math.sqrt(sum(b**2 for b in vector2))

        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0

        return dot_product / (magnitude1 * magnitude2)

    # Semantic search, it returns the 3 most similar notes based on the embedding
    def __semantic_search(self, embbedings: list, notes: list):
        scored = []

        for note in notes:
            note_embedding = note.get("embedding")

            if not note_embedding or len(note_embedding) == 0:
                continue

            score = self.__cosine_similarity(embbedings, note_embedding)

            if score > 0.4:
                scored.append((score, note))

        scored.sort(reverse=True, key=lambda x: x[0])

        return [note for _, note in scored[:5]]

    def __prepare_notes_for_llm(self, notes):
        return [{"title": note["title"], "content": note["content"]} for note in notes]
