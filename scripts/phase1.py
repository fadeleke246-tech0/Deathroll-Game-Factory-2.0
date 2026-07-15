#!/usr/bin/env python3
import sys
import time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts import config
from scripts import utils
from scripts.memory import memory

def main():
    print("🔍 PHASE 1: RESEARCH (with memory)")
    state = utils.load_json(config.DATA_DIR / "run_state.json")
    current_phase = state.get("phase")
    if current_phase is None:
        current_phase = 1
        state["phase"] = 1
        utils.save_json(state, config.DATA_DIR / "run_state.json")
        print("Initialized run_state.json with phase 1.")
    if current_phase != 1:
        print(f"Expected phase 1, got {current_phase}. Skipping.")
        return

    utils.send_telegram_admin("📊 Phase 1 started: researching game idea with memory...")

    best_practices = memory.retrieve_best_practices("shooter", limit=3)
    inspiration_text = ""
    if best_practices:
        inspiration_text = "\nPast successful games:\n" + "\n".join(
            [f"- {p['title']} ({p['genre']}): {p['concept']}" for p in best_practices[:3]]
        )

    prompt = f"""Propose a new HTML5 mobile game idea. Use the following inspiration from past successes if relevant:
{inspiration_text}

Output JSON:
{{
    "title": "Catchy short title",
    "genre": "shooter / soccer / racing / platformer / puzzle",
    "concept": "Brief 2-sentence concept",
    "inspiration": "Popular game it resembles"
}}"""
    try:
        response = utils.call_llm(prompt)
        idea = utils.extract_json_from_text(response)
        if not idea:
            raise ValueError("Invalid JSON")
    except Exception as e:
        utils.send_telegram_admin(f"❌ Phase 1 failed: {e}")
        sys.exit(1)

    game_id = idea['title'].lower().replace(' ', '_')
    msg = f"✅ Phase 1 complete\n\nTitle: {idea['title']}\nGenre: {idea['genre']}\nConcept: {idea['concept']}\nInspiration: {idea.get('inspiration', '')}"
    utils.send_telegram_admin(msg)

    memory.store_game({
        "id": game_id,
        "title": idea['title'],
        "genre": idea['genre'],
        "concept": idea['concept'],
        "inspiration": idea.get('inspiration', ''),
        "prompt": prompt,
        "timestamp": str(time.time())
    }, success_score=0.0)

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
