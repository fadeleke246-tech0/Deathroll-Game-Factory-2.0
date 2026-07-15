#!/usr/bin/env python3
"""
Daily consolidation: analyse all stored games, update success scores,
promote high‑performing patterns.
"""
import sys
import json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import config
from scripts.memory import memory

def main():
    print("🧠 BRAIN CONSOLIDATION")
    # Retrieve all games (we'll use a simple query)
    all_results = memory.collection.get()
    if not all_results or not all_results['ids']:
        print("No games in memory.")
        return

    # In real implementation, you'd compute success score based on plays/ratings.
    # For now, we just increment success for games with high ratings (simulated).
    for idx, doc_id in enumerate(all_results['ids']):
        metadata = all_results['metadatas'][idx]
        # Simulate feedback: if rating > 4, increase success
        rating = metadata.get('rating', 0)
        if rating >= 4:
            new_score = metadata.get('success', 0) + 0.1
            memory.update_success(doc_id, new_score)
            print(f"Updated {doc_id} success to {new_score}")

    print("Consolidation complete.")

if __name__ == "__main__":
    main()
