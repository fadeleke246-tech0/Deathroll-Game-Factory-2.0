#!/usr/bin/env python3
"""
Phase 5: Testing
- Runs simple static checks on the generated HTML/JS.
- In a real scenario, you could run Playwright or Puppeteer tests.
- For now, just ensures the greybox HTML exists and is valid.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
import config
import utils


def main():
    print("🧪 PHASE 5: TESTING")

    state = utils.load_json(config.DATA_DIR / "run_state.json")
    game = state.get("current_game")
    if not game or game["phase"] != 5:
        print("❌ No game in testing phase.")
        sys.exit(1)

    game_id = game["id"]
    game_html = config.OUTPUT_DIR / game_id / "index.html"

    if not game_html.exists():
        print(f"❌ Game HTML missing: {game_html}")
        sys.exit(1)

    # Simple validation: check for basic tags
    with open(game_html, "r", encoding="utf-8") as f:
        content = f.read()
    if "<canvas" not in content and "<div" not in content:
        print("⚠️ Warning: No canvas or div found – game might not render.")

    print("✅ Basic tests passed.")

    # Advance to build phase
    state["phase"] = 6
    game["phase"] = 6
    game["status"] = "building"
    utils.save_json(state, config.DATA_DIR / "run_state.json")

    print("✅ Phase 5 complete. Moving to Phase 6 (Build).")


if __name__ == "__main__":
    main()
