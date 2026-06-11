#!/usr/bin/env python3
"""
Phase 3: Greybox (no changes – code already generated in Phase 2).
Just ensure output folder exists.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
import config
import utils

def main():
    print("📦 PHASE 3: GREYBOX (code already generated)")
    state = utils.load_json(config.DATA_DIR / "run_state.json")
    game = state.get("current_game")
    if not game or game["phase"] != 3:
        print("❌ No game in greybox phase.")
        sys.exit(1)
    # The code already exists in output/<game_id>/index.html from Phase 2
    # We just advance the phase.
    state["phase"] = 4
    game["phase"] = 4
    game["status"] = "art_ready"
    utils.save_json(state, config.DATA_DIR / "run_state.json")
    print("✅ Phase 3 complete. Moving to Phase 4 (Art).")

if __name__ == "__main__":
    main()
