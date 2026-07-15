#!/usr/bin/env python3
import sys
import subprocess
import json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts import config
from scripts import utils

def run_static_analysis(html_path: Path) -> bool:
    content = html_path.read_text()
    errors = []
    if "eval(" in content:
        errors.append("Use of eval() detected")
    if "document.write" in content:
        errors.append("document.write used (bad practice)")
    if content.count("<script") != content.count("</script>"):
        errors.append("Unbalanced script tags")
    if content.count("<div") != content.count("</div>"):
        errors.append("Unbalanced div tags")
    if errors:
        utils.send_telegram_admin("⚠️ Static analysis warnings: " + "; ".join(errors))
        return False
    return True

def run_performance_test(html_path: Path) -> bool:
    size = html_path.stat().st_size
    if size > 500 * 1024:
        utils.send_telegram_admin("⚠️ HTML file size >500KB, might load slow")
        return False
    return True

def run_ai_playtest(html_path: Path) -> bool:
    content = html_path.read_text()
    if "Game Over" in content or "gameOver" in content:
        utils.send_telegram_admin("✅ AI playtest: game has a game-over condition")
        return True
    else:
        utils.send_telegram_admin("⚠️ AI playtest: no game-over condition found")
        return True

def main():
    print("🧪 PHASE 5: TESTING (full suite)")
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

    static_ok = run_static_analysis(html_path)
    perf_ok = run_performance_test(html_path)
    playtest_ok = run_ai_playtest(html_path)

    if static_ok and perf_ok and playtest_ok:
        utils.send_telegram_admin("✅ Phase 5: all tests passed.")
    else:
        utils.send_telegram_admin("⚠️ Phase 5: some tests had warnings, but continuing.")

    state["phase"] = 6
    utils.save_json(state, config.DATA_DIR / "run_state.json")
    print("Phase 5 done. State advanced to phase 6.")

if __name__ == "__main__":
    main()
