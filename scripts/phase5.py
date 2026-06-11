#!/usr/bin/env python3
"""
Phase 5: Automated testing. If test fails, attempt to fix by re‑running Phase 2.
"""
import sys
import subprocess
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import config
import utils

def run_html_check(html_path: Path) -> tuple[bool, str]:
    """Run basic HTML/CSS/JS checks."""
    if not html_path.exists():
        return False, "File missing"
    content = html_path.read_text()
    if "</html>" not in content:
        return False, "Missing closing </html>"
    if "canvas" not in content and "div" not in content:
        return False, "No render element found (canvas or div)"
    # Check for obvious JS syntax errors (very basic)
    if "function" not in content and "=>" not in content and "addEventListener" not in content:
        return False, "No interactive JavaScript found"
    return True, "OK"

def main():
    print("🧪 PHASE 5: TESTING")
    state = utils.load_json(config.DATA_DIR / "run_state.json")
    game = state.get("current_game")
    if not game or game["phase"] != 5:
        print("No game in phase 5.")
        sys.exit(1)

    game_id = game["id"]
    html_path = config.OUTPUT_DIR / game_id / "index.html"

    passed, msg = run_html_check(html_path)
    if not passed:
        print(f"❌ Test failed: {msg}")
        # Attempt self‑correction: re‑run Phase 2 with a more specific prompt
        game["phase"] = 2   # go back
        game["retries"] = game.get("retries", 0) + 1
        state["phase"] = 2
        utils.save_json(state, config.DATA_DIR / "run_state.json")
        print("🔄 Re‑running Phase 2 to fix the game...")
        # Call phase2.py
        subprocess.run([sys.executable, str(config.SCRIPTS_DIR / "phase2.py")], check=False)
        # After re‑run, we need to re‑enter phase 5. We'll let the workflow loop handle it.
        sys.exit(0)  # exit so workflow will re‑run from phase 2
    else:
        print("✅ All tests passed.")
        state["phase"] = 6
        game["phase"] = 6
        utils.save_json(state, config.DATA_DIR / "run_state.json")
        print("✅ Phase 5 complete. Moving to Phase 6 (Build).")

if __name__ == "__main__":
    main()
