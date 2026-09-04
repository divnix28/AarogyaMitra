import os
from typing import List
from sentence_transformers import SentenceTransformer

class VectorEmbedder:
    def __init__(self, model_name: str = None):
        self.model_name = model_name or os.getenv("EMBEDDING_MODEL_NAME", "sentence-transformers/all-MiniLM-L6-v2")
        self.model = SentenceTransformer(self.model_name)

    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        embeddings = self.model.encode(texts, show_progress_bar=False)
        return embeddings.tolist()