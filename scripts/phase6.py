#!/usr/bin/env python3
import shutil
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts import config
from scripts import utils

def main():
    print("🏗️ PHASE 6: BUILD")
    state = utils.load_json(config.DATA_DIR / "run_state.json")
    if state.get("phase") != 6:
        print(f"Expected phase 6, got {state.get('phase')}. Skipping.")
        return

    game = state["current_game"]
    utils.send_telegram_admin(f"📦 Phase 6 started: building PWA for '{game['title']}'...")

    src = config.OUTPUT_DIR / game["id"]
    dst = config.DOCS_DIR / game["id"]
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)

    if (dst / "game.html").exists() and not (dst / "index.html").exists():
        (dst / "game.html").rename(dst / "index.html")

    manifest = dst / "manifest.json"
    manifest.write_text(f'{{"name":"{game["title"]}","start_url":".","display":"standalone"}}')

    state["phase"] = 7
    utils.save_json(state, config.DATA_DIR / "run_state.json")
    utils.send_telegram_admin(f"✅ Phase 6 complete: game built at {config.PUBLIC_BASE_URL}/{game['id']}/")
    print("Phase 6 done. State advanced to phase 7.")

if __name__ == "__main__":
    main()
