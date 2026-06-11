#!/usr/bin/env python3
"""
Phase 7: Publish
- Sends a Telegram announcement about the new game.
- Optionally updates the storefront's "latest game" section.
"""

import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
import config
import utils


def main():
    print("📢 PHASE 7: PUBLISH")

    state = utils.load_json(config.DATA_DIR / "run_state.json")
    game = state.get("current_game")
    if not game or game["phase"] != 7:
        print("❌ No game in publish phase.")
        sys.exit(1)

    game_id = game["id"]
    title = game["title"]
    game_url = f"{config.PUBLIC_BASE_URL}/{game_id}/index.html"

    # Telegram announcement
    message = f"🎮 *New Game Released!*\n\n*{title}*\n{game['concept']}\n\nPlay now: {game_url}"
    if config.TELEGRAM_BOT_TOKEN and config.TELEGRAM_CHANNEL:
        success = utils.send_telegram_message(
            config.TELEGRAM_BOT_TOKEN,
            config.TELEGRAM_CHANNEL,
            message
        )
        if not success:
            print("⚠️ Telegram post failed (bot may not be admin).")
    else:
        print("⚠️ Telegram credentials missing. Skipping announcement.")

    # Update state: game cycle finished
    state["phase"] = 1  # Reset to start a new game
    state["current_game"] = None
    utils.save_json(state, config.DATA_DIR / "run_state.json")

    print("✅ Phase 7 complete. Factory ready for next game cycle.")


if __name__ == "__main__":
    main()
