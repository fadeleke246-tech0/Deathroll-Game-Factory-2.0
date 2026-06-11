#!/usr/bin/env python3
"""
Phase 1: Research
- Loads the game queue.
- Uses Gemini to propose a new game idea (genre, title, concept).
- Waits for manual approval or auto-approves after a timeout.
- Writes the approved idea to run_state.json and games_queue.json.
"""

import sys
import time
from pathlib import Path

# Add parent directory to path so we can import config and utils
sys.path.insert(0, str(Path(__file__).parent.parent))

import config
import utils
import google.generativeai as genai


def get_approval(idea_text: str, auto_minutes: int) -> bool:
    """
    Wait for user to type /approve in the GitHub Actions log,
    or auto-approve after auto_minutes minutes.
    """
    print("\n" + "="*60)
    print("PROPOSED GAME IDEA:")
    print(idea_text)
    print("="*60)
    print(f"You have {auto_minutes} minutes to approve by typing '/approve'.")
    print("Waiting...")

    start_time = time.time()
    deadline = start_time + (auto_minutes * 60)

    while time.time() < deadline:
        # Read from stdin (GitHub Actions allows input via workflow_dispatch)
        if sys.stdin in select.select([sys.stdin], [], [], 1)[0]:
            line = sys.stdin.readline().strip()
            if line == "/approve":
                print("✅ Manual approval received.")
                return True
        time.sleep(1)
    print(f"⏰ Auto-approving after {auto_minutes} minutes.")
    return True


def main():
    print("🔍 PHASE 1: RESEARCH")

    # 1. Load queue and state
    queue = utils.load_json(config.DATA_DIR / "games_queue.json")
    state = utils.load_json(config.DATA_DIR / "run_state.json")

    # 2. Configure Gemini
    if not config.GEMINI_API_KEY:
        print("❌ GEMINI_API_KEY not set.")
        sys.exit(1)
    genai.configure(api_key=config.GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-2.0-flash")

    # 3. Generate game idea
    prompt = """
    Propose a new web-based HTML5 game. Output in JSON format:
    {
        "genre": "one of: shooter, soccer, racing, platformer, puzzle, rpg",
        "title": "Game Title",
        "concept": "Brief 2-sentence concept"
    }
    """
    response = model.generate_content(prompt)
    idea_json = utils.extract_json_from_text(response.text)
    if not idea_json:
        print("❌ Failed to parse Gemini response.")
        sys.exit(1)

    # 4. Save proposed idea to state
    state["current_game"] = {
        "id": idea_json["title"].lower().replace(" ", "_"),
        "genre": idea_json["genre"],
        "title": idea_json["title"],
        "concept": idea_json["concept"],
        "phase": 1,
        "status": "proposed"
    }
    utils.save_json(state, config.DATA_DIR / "run_state.json")

    # 5. Approval step
    idea_text = f"Title: {idea_json['title']}\nGenre: {idea_json['genre']}\nConcept: {idea_json['concept']}"
    if not get_approval(idea_text, config.AUTO_APPROVE_WAIT_MINUTES):
        print("❌ Not approved. Exiting.")
        sys.exit(0)

    # 6. Move to queue and advance phase
    game_id = state["current_game"]["id"]
    queue[game_id] = {
        "title": idea_json["title"],
        "genre": idea_json["genre"],
        "concept": idea_json["concept"],
        "status": "planned",
        "promo_image": ""   # Will be filled in Phase 4
    }
    utils.save_json(queue, config.DATA_DIR / "games_queue.json")

    state["phase"] = 2
    state["current_game"]["phase"] = 2
    state["current_game"]["status"] = "planning"
    utils.save_json(state, config.DATA_DIR / "run_state.json")

    print("✅ Phase 1 complete. Moving to Phase 2 (Plan).")


if __name__ == "__main__":
    main()
