#!/usr/bin/env python3
import shutil
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
import config
import utils

def main():
    print("🏗️ PHASE 6: BUILD")
    state = utils.load_json(config.DATA_DIR / "run_state.json")
    game = state.get("current_game")
    if not game or game["phase"] != 6:
        print("No game in phase 6.")
        sys.exit(1)
    game_id = game["id"]
    src_dir = config.OUTPUT_DIR / game_id
    dst_dir = config.DOCS_DIR / game_id
    if dst_dir.exists():
        shutil.rmtree(dst_dir)
    shutil.copytree(src_dir, dst_dir)
    # Ensure index.html
    if (dst_dir / "game.html").exists() and not (dst_dir / "index.html").exists():
        (dst_dir / "game.html").rename(dst_dir / "index.html")
    # Create minimal manifest.json if missing
    manifest = dst_dir / "manifest.json"
    if not manifest.exists():
        manifest.write_text('{"name":"' + game["title"] + '","start_url":".","display":"standalone"}')
    # Update portfolio with final URL
    portfolio = utils.load_json(config.DATA_DIR / "portfolio.json")
    if game_id in portfolio:
        portfolio[game_id]["game_url"] = f"{config.PUBLIC_BASE_URL}/{game_id}/index.html"
        utils.save_json(portfolio, config.DATA_DIR / "portfolio.json")
    state["phase"] = 7
    game["phase"] = 7
    utils.save_json(state, config.DATA_DIR / "run_state.json")
    print(f"✅ Game built at {config.PUBLIC_BASE_URL}/{game_id}/")
    print("Phase 6 done. Moving to Phase 7 (Publish).")

if __name__ == "__main__":
    main()
