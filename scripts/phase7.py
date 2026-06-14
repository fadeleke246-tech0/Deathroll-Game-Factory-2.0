#!/usr/bin/env python3
import sys
import requests
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import config
from scripts import utils

def send_telegram_with_debug(bot_token: str, chat_id: str, text: str) -> bool:
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    try:
        r = requests.post(url, json=payload, timeout=10)
        print(f"Telegram response for {chat_id}: {r.status_code} - {r.text}")
        return r.status_code == 200
    except Exception as e:
        print(f"Exception: {e}")
        return False

def main():
    print("📢 PHASE 7: PUBLISH")
    state = utils.load_json(config.DATA_DIR / "run_state.json")
    if state.get("phase") != 7:
        print(f"Expected phase 7, got {state.get('phase')}. Skipping.")
        return

    game = state["current_game"]
    game_url = f"{config.PUBLIC_BASE_URL}/{game['id']}/index.html"
    msg = f"🎮 *New Game Released!*\n\n*{game['title']}*\n{game['concept']}\n\nPlay now: {game_url}"

    # Test channel
    if config.TELEGRAM_BOT_TOKEN and config.TELEGRAM_CHANNEL:
        print(f"Attempting to send to channel: {config.TELEGRAM_CHANNEL}")
        success = send_telegram_with_debug(config.TELEGRAM_BOT_TOKEN, config.TELEGRAM_CHANNEL, msg)
        if success:
            print("✅ Channel message sent.")
        else:
            print("❌ Channel message failed. Check channel ID and bot admin status.")
    else:
        print("⚠️ Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHANNEL")

    # Test admin DM
    if config.TELEGRAM_BOT_TOKEN and config.TELEGRAM_ADMIN_CHAT_ID:
        print(f"Attempting to send to admin: {config.TELEGRAM_ADMIN_CHAT_ID}")
        success = send_telegram_with_debug(config.TELEGRAM_BOT_TOKEN, config.TELEGRAM_ADMIN_CHAT_ID, f"✅ Game '{game['title']}' completed. URL: {game_url}")
        if success:
            print("✅ Admin message sent.")
        else:
            print("❌ Admin message failed. Check TELEGRAM_ADMIN_CHAT_ID (must be numeric ID).")
    else:
        print("⚠️ Missing TELEGRAM_BOT_TOKEN or TELEGRAM_ADMIN_CHAT_ID")

    # Update queue and reset state regardless of Telegram success
    queue = utils.load_json(config.DATA_DIR / "games_queue.json")
    if game["id"] in queue:
        queue[game["id"]]["status"] = "completed"
        utils.save_json(queue, config.DATA_DIR / "games_queue.json")

    state["phase"] = 1
    state.pop("current_game", None)
    utils.save_json(state, config.DATA_DIR / "run_state.json")
    print("✅ Factory reset to phase 1.")

if __name__ == "__main__":
    main()
