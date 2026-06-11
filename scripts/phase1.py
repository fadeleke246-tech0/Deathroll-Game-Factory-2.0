#!/usr/bin/env python3
"""
Phase 1: Research – propose a new game idea using LLM, wait for approval.
"""
import sys
import time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import config
import utils

def main():
    print("🔍 PHASE 1: RESEARCH")
    prompt = """
You are a game designer. Propose a new HTML5 mobile game idea that can be built in one day.
Output a JSON object with exactly these keys:
{
    "title": "Catchy short title",
    "genre": "shooter / soccer / racing / platformer / puzzle / fighting",
    "concept": "Brief 2‑sentence concept",
    "inspiration": "Popular game it resembles (e.g., Subway Surfers, Asphalt, Among Us)"
}
"""
    try:
        response = utils.call_llm(prompt)
        idea = utils.extract_json_from_text(response)
        if not idea:
            raise ValueError("Invalid JSON from LLM")
    except Exception as e:
        print(f"❌ LLM failed: {e}")
        sys.exit(1)

    print(f"\nProposed game: {idea['title']} ({idea['genre']})")
    print(f"Concept: {idea['concept']}")
    print(f"Inspired by: {idea.get('inspiration', 'unknown')}")
    print(f"\nWaiting for /approve or auto in {config.AUTO_APPROVE_WAIT_MINUTES} min...")

    # Approval polling (simulated via GitHub Actions input, but we'll auto‑approve after delay for automation)
    # In GitHub Actions, we cannot read stdin easily, so we auto‑approve after timeout.
    time.sleep(config.AUTO_APPROVE_WAIT_MINUTES * 60)
    print("✅ Auto‑approved.")

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
        "status": "researched",
        "retries": 0
    }
    utils.save_json(state, config.DATA_DIR / "run_state.json")

    # Update queue
    queue = utils.load_json(config.DATA_DIR / "games_queue.json")
    queue[game_id] = {"status": "planned", "title": idea['title']}
    utils.save_json(queue, config.DATA_DIR / "games_queue.json")

    # Advance to phase 2
    state["phase"] = 2
    state["current_game"]["phase"] = 2
    utils.save_json(state, config.DATA_DIR / "run_state.json")
    print("✅ Phase 1 complete. Moving to Phase 2.")

if __name__ == "__main__":
    main()
