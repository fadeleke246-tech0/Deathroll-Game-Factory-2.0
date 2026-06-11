#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import config
import utils

def main():
    print("🔍 PHASE 1: RESEARCH")
    state = utils.load_json(config.DATA_DIR / "run_state.json")
    if state.get("phase") != 1:
        print(f"Expected phase 1, got {state.get('phase')}. Skipping.")
        return

    utils.send_telegram_admin("📊 Phase 1 started: researching game idea...")

    prompt = """Propose a new HTML5 mobile game idea. Output JSON:
{
    "title": "Catchy short title",
    "genre": "shooter / soccer / racing / platformer / puzzle",
    "concept": "Brief 2-sentence concept",
    "inspiration": "Popular game it resembles"
}"""
    try:
        response = utils.call_llm(prompt)
        idea = utils.extract_json_from_text(response)
        if not idea:
            raise ValueError("Invalid JSON")
    except Exception as e:
        utils.send_telegram_admin(f"❌ Phase 1 failed: {e}")
        sys.exit(1)

    game_id = idea['title'].lower().replace(' ', '_')
    msg = f"✅ Phase 1 complete\n\nTitle: {idea['title']}\nGenre: {idea['genre']}\nConcept: {idea['concept']}\nInspiration: {idea.get('inspiration', '')}\n\nNext phase will run tomorrow (or manually)."
    utils.send_telegram_admin(msg)

    state["current_game"] = {
        "id": game_id,
        "title": idea['title'],
        "genre": idea['genre'],
        "concept": idea['concept'],
        "inspiration": idea.get('inspiration', '')
    }
    state["phase"] = 2
    utils.save_json(state, config.DATA_DIR / "run_state.json")

    queue = utils.load_json(config.DATA_DIR / "games_queue.json")
    queue[game_id] = {"status": "planned", "title": idea['title']}
    utils.save_json(queue, config.DATA_DIR / "games_queue.json")

    print("Phase 1 done. State advanced to phase 2.")

if __name__ == "__main__":
    main()
