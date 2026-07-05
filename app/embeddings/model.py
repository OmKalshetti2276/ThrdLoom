from __future__ import annotations

import numpy as np
from sentence_transformers import SentenceTransformer

from src.config import config


class Embedder:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._model = None
        return cls._instance

    def load(self):
        if self._model is None:
            self._model = SentenceTransformer(config.embedding_model)
        return self._model

    @property
    def model(self):
        if self._model is None:
            return self.load()
        return self._model

    def embed(self, text: str) -> list[float]:
        vec = self.model.encode(text, normalize_embeddings=True)
        return vec.tolist()

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        vecs = self.model.encode(texts, normalize_embeddings=True)
        return [v.tolist() for v in vecs]

    def similarity(self, a: list[float], b: list[float]) -> float:
        return float(np.dot(a, b))


embedder = Embedder()
