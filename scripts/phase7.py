#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
import config
import utils

def send_telegram_message(bot_token: str, chat_id: str, text: str):
    import requests
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    try:
        r = requests.post(url, json={"chat_id": chat_id, "text": text, "parse_mode": "Markdown"})
        return r.status_code == 200
    except:
        return False

def main():
    print("📢 PHASE 7: PUBLISH")
    state = utils.load_json(config.DATA_DIR / "run_state.json")
    game = state.get("current_game")
    if not game or game["phase"] != 7:
        print("No game in phase 7.")
        sys.exit(1)
    game_id = game["id"]
    game_url = f"{config.PUBLIC_BASE_URL}/{game_id}/index.html"
    message = f"🎮 *New Game Released!*\n\n*{game['title']}*\n{game['concept']}\n\nPlay: {game_url}"
    token = config.TELEGRAM_BOT_TOKEN if hasattr(config, 'TELEGRAM_BOT_TOKEN') else None
    if token:
        channel_id = getattr(config, 'TELEGRAM_CHANNEL', '@deathrollprod')
        send_telegram_message(token, channel_id, message)
        print("Telegram notification sent.")
    else:
        print("No Telegram token – skipping.")

    # Mark as completed in queue
    queue = utils.load_json(config.DATA_DIR / "games_queue.json")
    if game_id in queue:
        queue[game_id]["status"] = "completed"
        utils.save_json(queue, config.DATA_DIR / "games_queue.json")

    # Reset state for next game
    state["phase"] = 1
    state.pop("current_game", None)
    utils.save_json(state, config.DATA_DIR / "run_state.json")
    print("✅ Game cycle complete. Ready for next genre.")

if __name__ == "__main__":
    main()
