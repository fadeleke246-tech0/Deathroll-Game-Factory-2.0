#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
import config
import utils

def main():
    print("📐 PHASE 2: GENERATE GAME")
    state = utils.load_json(config.DATA_DIR / "run_state.json")
    game = state.get("current_game")
    if not game or game["phase"] != 2:
        print("No game in phase 2.")
        sys.exit(1)

    prompt = f"""
You are an expert HTML5 game developer. Write a complete, self-contained HTML document that implements a {game['genre']} game titled "{game['title']}".
Concept: {game['concept']}
Inspiration: {game.get('inspiration', '')}

Requirements:
- Use canvas, vanilla JS, no external libs.
- Include score, lives, game over, restart.
- Support both mouse and touch.
- Use placeholder images: assets/player.png, assets/enemy.png, assets/background.png, assets/bullet.png (if needed). The game should fallback to colored shapes if images fail to load.
- Output only the HTML code, no extra text.
"""
    code = utils.call_llm_with_fallback(prompt)
    # Clean markdown if present
    if "```html" in code:
        code = code.split("```html")[1].split("```")[0]
    game_id = game["id"]
    out_dir = config.OUTPUT_DIR / game_id
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "index.html").write_text(code)

    # Save plan metadata (for art generation)
    plan = {"assets": ["player", "enemy", "background", "bullet"]}
    utils.save_json(plan, out_dir / "game_plan.json")

    state["phase"] = 3
    game["phase"] = 3
    utils.save_json(state, config.DATA_DIR / "run_state.json")
    print("✅ Phase 2 done. Moving to Phase 3.")

if __name__ == "__main__":
    main()
