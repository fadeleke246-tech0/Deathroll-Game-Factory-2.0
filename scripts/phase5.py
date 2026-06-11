#!/usr/bin/env python3
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
        print("No game in phase 5.")
        sys.exit(1)
    game_id = game["id"]
    index = config.OUTPUT_DIR / game_id / "index.html"
    if not index.exists():
        print("Missing index.html – test failed")
        sys.exit(1)
    # Basic HTML presence check
    if "</html>" not in index.read_text():
        print("Incomplete HTML")
        sys.exit(1)
    print("Basic test passed.")
    state["phase"] = 6
    game["phase"] = 6
    utils.save_json(state, config.DATA_DIR / "run_state.json")
    print("✅ Phase 5 done. Moving to Phase 6 (Build).")

if __name__ == "__main__":
    main()
