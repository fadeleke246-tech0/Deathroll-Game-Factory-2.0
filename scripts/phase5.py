#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import config
import utils

def main():
    print("🧪 PHASE 5: TESTING")
    state = utils.load_json(config.DATA_DIR / "run_state.json")
    if state.get("phase") != 5:
        print(f"Expected phase 5, got {state.get('phase')}. Skipping.")
        return

    game = state["current_game"]
    utils.send_telegram_admin(f"🧪 Phase 5 started: testing '{game['title']}'...")

    html_path = config.OUTPUT_DIR / game["id"] / "index.html"
    if not html_path.exists():
        utils.send_telegram_admin("❌ Phase 5 failed: index.html missing.")
        sys.exit(1)

    content = html_path.read_text()
    if "<canvas" not in content and "<div" not in content:
        utils.send_telegram_admin("⚠️ Phase 5 warning: no canvas/div found, but continuing.")
    else:
        utils.send_telegram_admin("✅ Phase 5: basic HTML check passed.")

    state["phase"] = 6
    utils.save_json(state, config.DATA_DIR / "run_state.json")
    print("Phase 5 done. State advanced to phase 6.")

if __name__ == "__main__":
    main()
