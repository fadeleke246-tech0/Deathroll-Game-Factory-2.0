#!/usr/bin/env python3
"""
Phase 6: Build PWA and copy game to docs/ for GitHub Pages.
"""
import shutil
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import config
import utils

def create_pwa_files(game_dir: Path, title: str):
    manifest = game_dir / "manifest.json"
    if not manifest.exists():
        manifest.write_text(f'{{"name":"{title}","short_name":"{title[:12]}","start_url":".","display":"standalone"}}')
    sw = game_dir / "sw.js"
    if not sw.exists():
        sw.write_text('self.addEventListener("install",e=>e.waitUntil(self.skipWaiting()));self.addEventListener("fetch",e=>e.respondWith(fetch(e.request)));')

def main():
    print("🏗️ PHASE 6: BUILD & DEPLOY")
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

    # Ensure index.html is correctly named
    if (dst_dir / "game.html").exists() and not (dst_dir / "index.html").exists():
        (dst_dir / "game.html").rename(dst_dir / "index.html")

    create_pwa_files(dst_dir, game["title"])

    # Update portfolio with final URL
    portfolio = utils.load_json(config.DATA_DIR / "portfolio.json")
    if game_id in portfolio:
        portfolio[game_id]["game_url"] = f"{config.PUBLIC_BASE_URL}/{game_id}/index.html"
        utils.save_json(portfolio, config.DATA_DIR / "portfolio.json")

    state["phase"] = 7
    game["phase"] = 7
    utils.save_json(state, config.DATA_DIR / "run_state.json")
    print(f"✅ Game deployed to {config.PUBLIC_BASE_URL}/{game_id}/")
    print("Phase 6 complete. Moving to Phase 7 (Publish).")

if __name__ == "__main__":
    main()
