#!/usr/bin/env python3
"""
Phase 7: Publish game announcement to Telegram, reset factory for next game.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import config
import utils

def main():
    print("📢 PHASE 7: PUBLISH")
    state = utils.load_json(config.DATA_DIR / "run_state.json")
    game = state.get("current_game")
    if not game or game["phase"] != 7:
        print("No game in phase 7.")
        sys.exit(1)

    game_id = game["id"]
    game_url = f"{config.PUBLIC_BASE_URL}/{game_id}/index.html"
    message = f"🎮 *New Game Released!*\n\n*{game['title']}*\n{game['concept']}\n\nPlay now: {game_url}"
    utils.send_telegram_message(message)

    # Mark as completed in queue
    queue = utils.load_json(config.DATA_DIR / "games_queue.json")
    if game_id in queue:
        queue[game_id]["status"] = "completed"
        utils.save_json(queue, config.DATA_DIR / "games_queue.json")

    # Reset for next game (but keep queue for future)
    state["phase"] = 1
    state.pop("current_game", None)
    utils.save_json(state, config.DATA_DIR / "run_state.json")
    print("✅ Game cycle complete. Ready for next genre.")

if __name__ == "__main__":
    main()
