#!/usr/bin/env python3
"""
Phase 2: Plan
- Uses Gemini to generate a detailed game_plan.json:
  mechanics, controls, assets needed, HTML/CSS/JS structure.
- Saves the plan inside output/<game_id>/game_plan.json
"""

import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
import config
import utils
import google.generativeai as genai


def main():
    print("📐 PHASE 2: PLAN")

    state = utils.load_json(config.DATA_DIR / "run_state.json")
    game = state.get("current_game")
    if not game or game["phase"] != 2:
        print("❌ No game in planning phase.")
        sys.exit(1)

    game_id = game["id"]
    genre = game["genre"]
    title = game["title"]
    concept = game["concept"]

    # Create output folder for this game
    game_output_dir = config.OUTPUT_DIR / game_id
    game_output_dir.mkdir(parents=True, exist_ok=True)

    # 1. Generate plan using Gemini
    if not config.GEMINI_API_KEY:
        print("❌ GEMINI_API_KEY not set.")
        sys.exit(1)
    genai.configure(api_key=config.GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-2.0-flash")

    prompt = f"""
    You are a game designer. Create a detailed technical plan for a {genre} game titled "{title}".
    Concept: {concept}

    Output a JSON object with the following structure:
    {{
        "mechanics": "Description of core game loop and rules",
        "controls": "Keyboard/mouse/touch controls",
        "assets": {{
            "images": ["list of required image filenames"],
            "sounds": ["list of sound filenames (optional)"]
        }},
        "structure": {{
            "html_elements": ["main canvas", "UI divs"],
            "javascript_modules": ["game logic", "input handler", "renderer"]
        }},
        "victory_condition": "How the player wins",
        "difficulty_curve": "How difficulty scales"
    }}
    """
    response = model.generate_content(prompt)
    plan = utils.extract_json_from_text(response.text)
    if not plan:
        print("❌ Failed to generate plan.")
        sys.exit(1)

    # 2. Save plan
    plan_path = game_output_dir / "game_plan.json"
    utils.save_json(plan, plan_path)
    print(f"✅ Plan saved to {plan_path}")

    # 3. Update state and queue
    queue = utils.load_json(config.DATA_DIR / "games_queue.json")
    if game_id in queue:
        queue[game_id]["plan"] = plan_path.name
        utils.save_json(queue, config.DATA_DIR / "games_queue.json")

    state["phase"] = 3
    game["phase"] = 3
    game["status"] = "greybox"
    utils.save_json(state, config.DATA_DIR / "run_state.json")

    print("✅ Phase 2 complete. Moving to Phase 3 (Greybox).")


if __name__ == "__main__":
    main()
