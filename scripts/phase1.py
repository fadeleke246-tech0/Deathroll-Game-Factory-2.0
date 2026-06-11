#!/usr/bin/env python3
import sys
import time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
import config
import utils

def main():
    print("🔍 PHASE 1: RESEARCH")
    prompt = """
Propose a new HTML5 mobile game idea. Output JSON:
{
    "title": "Catchy title",
    "genre": "shooter/soccer/racing/platformer/puzzle",
    "concept": "Brief concept (2 sentences)",
    "inspiration": "Popular game it resembles (e.g., Subway Surfers)"
}
"""
    response = utils.call_llm_with_fallback(prompt)
    idea = utils.extract_json_from_text(response)
    if not idea:
        print("❌ Failed to parse idea. Exiting.")
        sys.exit(1)

    print(f"\nProposed game: {idea['title']} ({idea['genre']})\n{idea['concept']}")
    print(f"Waiting for /approve or auto in {config.AUTO_APPROVE_WAIT_MINUTES} min...")
    start = time.time()
    approved = False
    while time.time() - start < config.AUTO_APPROVE_WAIT_MINUTES * 60:
        if sys.stdin in [sys.stdin]:
            line = sys.stdin.readline().strip()
            if line == "/approve":
                approved = True
                break
        time.sleep(1)
    if not approved:
        print("Auto‑approving.")

    # Save to state
    game_id = idea['title'].lower().replace(' ', '_')
    state = utils.load_json(config.DATA_DIR / "run_state.json")
    state["current_game"] = {
        "id": game_id,
        "title": idea['title'],
        "genre": idea['genre'],
        "concept": idea['concept'],
        "inspiration": idea.get('inspiration', ''),
        "phase": 1,
        "status": "researched"
    }
    utils.save_json(state, config.DATA_DIR / "run_state.json")
    # Also initialise queue
    queue = utils.load_json(config.DATA_DIR / "games_queue.json")
    queue[game_id] = {"status": "planned", "title": idea['title']}
    utils.save_json(queue, config.DATA_DIR / "games_queue.json")

    state["phase"] = 2
    utils.save_json(state, config.DATA_DIR / "run_state.json")
    print("✅ Phase 1 done. Move to Phase 2.")

if __name__ == "__main__":
    main()
