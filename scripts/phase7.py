#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import config
import utils

def main():
    print("📢 PHASE 7: PUBLISH")
    state = utils.load_json(config.DATA_DIR / "run_state.json")
    if state.get("phase") != 7:
        print(f"Expected phase 7, got {state.get('phase')}. Skipping.")
        return

    game = state["current_game"]
    game_url = f"{config.PUBLIC_BASE_URL}/{game['id']}/index.html"
    msg = f"🎮 *New Game Released!*\n\n*{game['title']}*\n{game['concept']}\n\nPlay now: {game_url}"
    utils.send_telegram_channel(msg)
    utils.send_telegram_admin(f"✅ Phase 7 complete: game announced in channel.")

    queue = utils.load_json(config.DATA_DIR / "games_queue.json")
    if game["id"] in queue:
        queue[game["id"]]["status"] = "completed"
        utils.save_json(queue, config.DATA_DIR / "games_queue.json")

    # Reset for next game
    state["phase"] = 1
    state.pop("current_game", None)
    utils.save_json(state, config.DATA_DIR / "run_state.json")
    utils.send_telegram_admin("🏭 Factory ready for next game. Phase reset to 1.")

    print("✅ Factory cycle complete. Ready for next game.")

if __name__ == "__main__":
    main()
