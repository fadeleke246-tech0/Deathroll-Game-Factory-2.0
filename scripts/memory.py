"""
Memory module using ChromaDB for long‑term storage and retrieval of game patterns,
user feedback, and successful prompts.
"""
import json
import uuid
import time
from pathlib import Path
from typing import List, Dict, Optional

import chromadb
from chromadb.utils import embedding_functions

import config

class GameMemory:
    def __init__(self, persist_dir: str = "data/chroma"):
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.embedding_fn = embedding_functions.DefaultEmbeddingFunction()
        self.collection = self.client.get_or_create_collection(
            name="game_memory",
            embedding_function=self.embedding_fn
        )

    def store_game(self, game_data: Dict, success_score: float = 0.0) -> str:
        doc_id = game_data.get("id") or str(uuid.uuid4())
        document = json.dumps(game_data)
        metadata = {
            "title": game_data.get("title", ""),
            "genre": game_data.get("genre", ""),
            "success": success_score,
            "timestamp": game_data.get("timestamp", str(time.time())),
            "plays": game_data.get("plays", 0),
            "rating": game_data.get("rating", 0)
        }
        self.collection.add(
            ids=[doc_id],
            documents=[document],
            metadatas=[metadata]
        )
        return doc_id

    def retrieve_best_practices(self, genre: str, limit: int = 5) -> List[Dict]:
        results = self.collection.query(
            query_texts=[genre],
            n_results=limit,
            where={"genre": genre}
        )
        docs = results.get("documents", [[]])[0]
        return [json.loads(d) for d in docs if d]

    def update_success(self, game_id: str, new_score: float):
        self.collection.update(
            ids=[game_id],
            metadatas=[{"success": new_score}]
        )

    def get_high_performing_prompts(self, genre: str, top_k: int = 3) -> List[str]:
        results = self.collection.query(
            query_texts=[genre],
            n_results=top_k,
            where={"genre": genre},
            order_by="success"
        )
        docs = results.get("documents", [[]])[0]
        prompts = []
        for d in docs:
            data = json.loads(d)
            if "prompt" in data:
                prompts.append(data["prompt"])
        return prompts

memory = GameMemory()
