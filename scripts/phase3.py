#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts import config
from scripts import utils

def main():
    print("📦 PHASE 3: GREYBOX")
    state = utils.load_json(config.DATA_DIR / "run_state.json")
    if state.get("phase") != 3:
        print(f"Expected phase 3, got {state.get('phase')}. Skipping.")
        return

    game = state["current_game"]
    utils.send_telegram_admin(f"🛠️ Phase 3 started: validating HTML for '{game['title']}'...")

    html_path = config.OUTPUT_DIR / game["id"] / "index.html"
    if not html_path.exists():
        utils.send_telegram_admin("❌ Phase 3 failed: index.html missing.")
        sys.exit(1)

    content = html_path.read_text()
    if "</html>" not in content:
        utils.send_telegram_admin("⚠️ Phase 3 warning: incomplete HTML, but continuing.")
    else:
        utils.send_telegram_admin("✅ Phase 3: HTML valid.")

    state["phase"] = 4
    utils.save_json(state, config.DATA_DIR / "run_state.json")
    print("Phase 3 done. State advanced to phase 4.")

if __name__ == "__main__":
    main()
