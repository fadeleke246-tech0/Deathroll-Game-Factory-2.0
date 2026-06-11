#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
import config
import utils

def main():
    print("📦 PHASE 3: GREYBOX (code already ready)")
    state = utils.load_json(config.DATA_DIR / "run_state.json")
    game = state.get("current_game")
    if not game or game["phase"] != 3:
        print("No game in phase 3.")
        sys.exit(1)
    # Phase 2 already wrote the HTML; we just advance.
    state["phase"] = 4
    game["phase"] = 4
    utils.save_json(state, config.DATA_DIR / "run_state.json")
    print("✅ Phase 3 done. Moving to Phase 4 (Art).")

if __name__ == "__main__":
    main()
