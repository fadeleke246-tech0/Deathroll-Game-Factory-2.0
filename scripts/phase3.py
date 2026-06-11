#!/usr/bin/env python3
"""
Phase 3: Greybox – ensure the generated HTML is valid and ready.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import config
import utils

def main():
    print("📦 PHASE 3: GREYBOX VALIDATION")
    state = utils.load_json(config.DATA_DIR / "run_state.json")
    game = state.get("current_game")
    if not game or game["phase"] != 3:
        print("No game in phase 3.")
        sys.exit(1)

    game_id = game["id"]
    html_path = config.OUTPUT_DIR / game_id / "index.html"
    if not html_path.exists():
        print("❌ index.html missing. Aborting.")
        sys.exit(1)

    content = html_path.read_text()
    # Basic checks
    if "<canvas" not in content and "<div" not in content:
        print("⚠️ Warning: No canvas or div found – game might not render.")
    if "</html>" not in content:
        print("❌ Invalid HTML – missing closing tag.")
        sys.exit(1)

    state["phase"] = 4
    game["phase"] = 4
    utils.save_json(state, config.DATA_DIR / "run_state.json")
    print("✅ Phase 3 complete. Moving to Phase 4 (Art).")

if __name__ == "__main__":
    main()
