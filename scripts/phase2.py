#!/usr/bin/env python3
"""
Phase 2: Generate the full HTML5 game code using LLM.
"""
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
- Use canvas and vanilla JavaScript (no external libraries).
- Include score, lives, game over, restart button.
- Support both mouse and touch (for mobile).
- Use placeholder images: assets/player.png, assets/enemy.png, assets/background.png, assets/bullet.png (if applicable). The game must fallback to coloured shapes if images fail to load.
- The game should be fully functional, fun, and polished.
- Output ONLY the HTML code, no extra text.
"""
    try:
        code = utils.call_llm(prompt, max_retries=config.MAX_RETRIES)
        # Clean markdown if present
        if "```html" in code:
            code = code.split("```html")[1].split("```")[0]
        elif "```" in code:
            code = code.split("```")[1]
    except Exception as e:
        print(f"❌ LLM code generation failed: {e}")
        # Retry once more with a simpler prompt
        prompt_simple = f"Write a simple but complete HTML5 canvas game with title '{game['title']}', genre {game['genre']}. Include score, lives, restart. Output only HTML."
        try:
            code = utils.call_llm(prompt_simple)
            if "```html" in code:
                code = code.split("```html")[1].split("```")[0]
        except Exception as e2:
            print(f"❌ Fallback also failed: {e2}")
            sys.exit(1)

    game_id = game["id"]
    out_dir = config.OUTPUT_DIR / game_id
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "index.html").write_text(code, encoding="utf-8")

    # Generate a simple plan for assets (Phase 4 will extract from HTML)
    plan = {"assets": ["player", "enemy", "background", "bullet"]}
    utils.save_json(plan, out_dir / "game_plan.json")

    state["phase"] = 3
    game["phase"] = 3
    utils.save_json(state, config.DATA_DIR / "run_state.json")
    print("✅ Phase 2 complete. Moving to Phase 3.")

if __name__ == "__main__":
    main()
