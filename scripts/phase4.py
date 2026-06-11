#!/usr/bin/env python3
"""
Phase 4: Art & Audio
- Generates a promo image using Pollinations.ai (with fallback).
- Optionally generates placeholder audio (skip for now).
- Updates portfolio.json and games_queue.json with the public image URL.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
import config
import utils


def main():
    print("🎨 PHASE 4: ART & AUDIO")

    state = utils.load_json(config.DATA_DIR / "run_state.json")
    game = state.get("current_game")
    if not game or game["phase"] != 4:
        print("❌ No game in art phase.")
        sys.exit(1)

    game_id = game["id"]
    title = game["title"]
    concept = game["concept"]

    # 1. Generate promo image
    prompt = f"Promotional image for a {game['genre']} game titled '{title}'. {concept}"
    # Save directly into docs/ so it's web-accessible
    promo_local_path = config.DOCS_DIR / f"promo_{game_id}.png"
    if utils.generate_image(prompt, promo_local_path):
        # Public URL (GitHub Pages)
        public_url = f"{config.PUBLIC_BASE_URL}/promo_{game_id}.png"
    else:
        print("⚠️ Using fallback placeholder URL")
        public_url = ""  # will be handled by storefront

    # 2. Update portfolio.json
    portfolio = utils.load_json(config.DATA_DIR / "portfolio.json")
    portfolio[game_id] = {
        "title": title,
        "genre": game["genre"],
        "concept": concept,
        "promo": public_url,
        "game_url": f"{config.PUBLIC_BASE_URL}/{game_id}/index.html",
        "status": "art_done"
    }
    utils.save_json(portfolio, config.DATA_DIR / "portfolio.json")

    # 3. Update games_queue.json
    queue = utils.load_json(config.DATA_DIR / "games_queue.json")
    if game_id in queue:
        queue[game_id]["promo_image"] = public_url
        queue[game_id]["status"] = "art_done"
        utils.save_json(queue, config.DATA_DIR / "games_queue.json")

    # 4. Update state
    state["phase"] = 5
    game["phase"] = 5
    game["status"] = "testing"
    utils.save_json(state, config.DATA_DIR / "run_state.json")

    print("✅ Phase 4 complete. Moving to Phase 5 (Testing).")


if __name__ == "__main__":
    main()
