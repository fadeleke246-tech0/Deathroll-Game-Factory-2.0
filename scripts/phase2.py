#!/usr/bin/env python3
"""
Phase 2: Generate complete game code (HTML/CSS/JS) based on research.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
import config
import utils
import google.generativeai as genai

def main():
    print("📐 PHASE 2: GENERATE GAME CODE")
    state = utils.load_json(config.DATA_DIR / "run_state.json")
    game = state.get("current_game")
    if not game or game["phase"] != 2:
        print("❌ No game in planning phase.")
        sys.exit(1)

    if not config.GEMINI_API_KEY:
        print("❌ GEMINI_API_KEY not set.")
        sys.exit(1)
    genai.configure(api_key=config.GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-2.0-flash")

    # Build a powerful prompt that asks for a complete, ready-to-run HTML5 game.
    prompt = f"""
You are an expert HTML5 game developer. Write a complete, self-contained HTML document that implements a game inspired by "{game['inspiration']}".

Game title: {game['title']}
Genre: {game['genre']}
Concept: {game['concept']}
Core mechanic: {game['core_mechanic']}

Requirements:
- Use HTML, CSS, and JavaScript (no external libraries unless necessary).
- Include a canvas element for rendering.
- Implement full game logic (collisions, scoring, game over, restart).
- Must be playable on both desktop (keyboard/mouse) and mobile (touch).
- Include a score display and a restart button or automatic restart.
- Use placeholder images with the following filenames: player.png, enemy.png, background.png, bullet.png (if applicable). The game should attempt to load these from "assets/" folder, but fallback to colored shapes if images are missing.
- The game should be complete, engaging, and polished – similar in depth to a simple arcade game.
- Output **only** the HTML code, no extra explanation.

Write the game now.
"""
    response = model.generate_content(prompt)
    game_code = response.text.strip()
    if not game_code.startswith("<!DOCTYPE html>"):
        # Sometimes Gemini adds markdown, clean it
        if "```html" in game_code:
            game_code = game_code.split("```html")[1].split("```")[0]
        elif "```" in game_code:
            game_code = game_code.split("```")[1]

    # Save the generated code
    game_id = game["id"]
    game_output_dir = config.OUTPUT_DIR / game_id
    game_output_dir.mkdir(parents=True, exist_ok=True)
    index_path = game_output_dir / "index.html"
    index_path.write_text(game_code, encoding="utf-8")
    print(f"✅ Game code written to {index_path}")

    # Save plan metadata (for art generation)
    plan = {
        "game_title": game["title"],
        "genre": game["genre"],
        "concept": game["concept"],
        "inspiration": game["inspiration"],
        "assets": ["player", "enemy", "background", "bullet"]  # You can ask Gemini to specify these
    }
    utils.save_json(plan, game_output_dir / "game_plan.json")

    # Update state
    state["phase"] = 3
    game["phase"] = 3
    game["status"] = "code_generated"
    utils.save_json(state, config.DATA_DIR / "run_state.json")
    print("✅ Phase 2 complete. Moving to Phase 3 (Art injection).")

if __name__ == "__main__":
    main()
