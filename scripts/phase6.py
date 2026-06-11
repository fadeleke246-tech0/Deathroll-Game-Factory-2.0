#!/usr/bin/env python3
"""
Phase 6: Build
- Copies the game from output/<game_id>/ to docs/<game_id>/
- Creates PWA manifest and service worker (optional).
- Does NOT commit; the workflow handles git add/commit.
"""

import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
import config
import utils


def create_pwa_files(dest_dir: Path, game_title: str):
    """Generate a minimal manifest.json and service worker."""
    manifest = {
        "name": game_title,
        "short_name": game_title[:12],
        "start_url": ".",
        "display": "standalone",
        "theme_color": "#000000",
        "background_color": "#ffffff",
        "icons": []
    }
    utils.save_json(manifest, dest_dir / "manifest.json")

    sw_js = """
self.addEventListener('install', event => {
    console.log('Service worker installed');
});
self.addEventListener('fetch', event => {
    event.respondWith(fetch(event.request));
});
"""
    (dest_dir / "sw.js").write_text(sw_js)
    print("📱 PWA files created.")


def main():
    print("🏗️ PHASE 6: BUILD")

    state = utils.load_json(config.DATA_DIR / "run_state.json")
    game = state.get("current_game")
    if not game or game["phase"] != 6:
        print("❌ No game in build phase.")
        sys.exit(1)

    game_id = game["id"]
    output_dir = config.OUTPUT_DIR / game_id
    docs_game_dir = config.DOCS_DIR / game_id

    # Copy game files
    if not utils.copy_game_to_docs(game_id, config.OUTPUT_DIR, config.DOCS_DIR):
        print("❌ Failed to copy game to docs/")
        sys.exit(1)

    # Create PWA files
    create_pwa_files(docs_game_dir, game["title"])

    # Update portfolio.json with final game URL
    portfolio = utils.load_json(config.DATA_DIR / "portfolio.json")
    if game_id in portfolio:
        portfolio[game_id]["game_url"] = f"{config.PUBLIC_BASE_URL}/{game_id}/index.html"
        portfolio[game_id]["status"] = "published"
        utils.save_json(portfolio, config.DATA_DIR / "portfolio.json")

    # Update queue
    queue = utils.load_json(config.DATA_DIR / "games_queue.json")
    if game_id in queue:
        queue[game_id]["status"] = "completed"
        utils.save_json(queue, config.DATA_DIR / "games_queue.json")

    # Advance to publish phase
    state["phase"] = 7
    game["phase"] = 7
    game["status"] = "publishing"
    utils.save_json(state, config.DATA_DIR / "run_state.json")

    print("✅ Phase 6 complete. Moving to Phase 7 (Publish).")


if __name__ == "__main__":
    main()
