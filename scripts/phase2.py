#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import config
import utils

def main():
    print("📐 PHASE 2: PLAN & CODE")
    state = utils.load_json(config.DATA_DIR / "run_state.json")
    if state.get("phase") != 2:
        print(f"Expected phase 2, got {state.get('phase')}. Skipping.")
        return

    game = state["current_game"]
    utils.send_telegram_admin(f"🎮 Phase 2 started: generating code for '{game['title']}'...")

    prompt = f"""
Write a complete HTML5 canvas game titled "{game['title']}", genre {game['genre']}.
Concept: {game['concept']}
Include score, lives, restart, touch+mouse support.
Use placeholder images: assets/player.png, assets/enemy.png, assets/background.png, assets/bullet.png.
Fallback to colored shapes if images missing.
Output only the HTML code.
"""
    try:
        code = utils.call_llm(prompt)
        if "```html" in code:
            code = code.split("```html")[1].split("```")[0]
    except Exception as e:
        utils.send_telegram_admin(f"❌ Phase 2 failed: {e}")
        sys.exit(1)

    game_dir = config.OUTPUT_DIR / game["id"]
    game_dir.mkdir(parents=True, exist_ok=True)
    (game_dir / "index.html").write_text(code)

    plan = {"assets": ["player", "enemy", "background", "bullet"]}
    utils.save_json(plan, game_dir / "game_plan.json")

    state["phase"] = 3
    utils.save_json(state, config.DATA_DIR / "run_state.json")
    utils.send_telegram_admin(f"✅ Phase 2 complete: game code generated. Moving to Phase 3 tomorrow.")
    print("Phase 2 done. State advanced to phase 3.")

if __name__ == "__main__":
    main()
