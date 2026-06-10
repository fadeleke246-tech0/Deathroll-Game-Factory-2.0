import json
import requests
import time
from pathlib import Path
import sys
import os

# Add parent directory to path so we can import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

# ------------------- Telegram -------------------
def send_telegram(chat_id, text, parse_mode="HTML"):
    """Send message to a Telegram chat (DM or channel)"""
    url = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": parse_mode,
        "disable_web_page_preview": True
    }
    try:
        r = requests.post(url, json=payload, timeout=30)
        r.raise_for_status()
        return True
    except Exception as e:
        print(f"Telegram send error: {e}")
        return False

def send_to_admin(text):
    """Send report to developer's DM"""
    return send_telegram(config.TELEGRAM_ADMIN_CHAT_ID, text)

def send_to_channel(text):
    """Send final game post to public channel"""
    return send_telegram(config.TELEGRAM_CHANNEL_ID, text)

# ------------------- File helpers -------------------
def load_json(filepath):
    if not os.path.exists(filepath):
        return {}
    with open(filepath, "r") as f:
        return json.load(f)

def save_json(filepath, data):
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)

# ------------------- Game Queue -------------------
def get_current_game():
    """Returns (genre, index) of the game currently being processed"""
    queue = load_json(config.GAMES_QUEUE_FILE)
    if not queue or "games" not in queue:
        return None, -1
    for idx, game in enumerate(queue["games"]):
        if game.get("status") not in ["completed", "skipped"]:
            return game, idx
    return None, -1

def update_game_status(genre, status, meta=None):
    queue = load_json(config.GAMES_QUEUE_FILE)
    for game in queue.get("games", []):
        if game["genre"] == genre:
            game["status"] = status
            if meta:
                game.update(meta)
            break
    save_json(config.GAMES_QUEUE_FILE, queue)

def mark_game_completed(genre, game_url, promo_image_url):
    update_game_status(genre, "completed", {
        "completed_at": time.time(),
        "game_url": game_url,
        "promo_image": promo_image_url
    })
    # Also add to portfolio
    portfolio = load_json(config.PORTFOLIO_FILE)
    if "games" not in portfolio:
        portfolio["games"] = []
    portfolio["games"].append({
        "genre": genre,
        "url": game_url,
        "promo": promo_image_url,
        "date": time.time()
    })
    save_json(config.PORTFOLIO_FILE, portfolio)

# ------------------- Phase state -------------------
def get_phase_state():
    """Return current phase (1-7) and any metadata"""
    state = load_json(config.RUN_STATE_FILE)
    return state.get("phase", 1), state.get("phase_data", {})

def set_phase_state(phase, phase_data=None):
    state = load_json(config.RUN_STATE_FILE)
    state["phase"] = phase
    if phase_data:
        state["phase_data"] = phase_data
    else:
        state["phase_data"] = {}
    save_json(config.RUN_STATE_FILE, state)

# ------------------- Art helpers -------------------
def generate_image(prompt, output_path, width=512, height=512):
    """
    Use Pollinations.ai (free, no key) to generate image.
    Falls back to PIL if Pollinations fails.
    """
    # Pollinations URL format
    url = f"https://image.pollinations.ai/prompt/{requests.utils.quote(prompt)}?width={width}&height={height}"
    try:
        resp = requests.get(url, timeout=60)
        if resp.status_code == 200:
            with open(output_path, "wb") as f:
                f.write(resp.content)
            return True
    except Exception as e:
        print(f"Pollinations error: {e}")
    
    # Fallback: create a solid color image with text using PIL
    try:
        from PIL import Image, ImageDraw, ImageFont
        img = Image.new('RGB', (width, height), color=(73, 109, 137))
        d = ImageDraw.Draw(img)
        # Use default font
        d.text((10, height//2), prompt[:50], fill=(255,255,255))
        img.save(output_path)
        return True
    except ImportError:
        print("PIL not available, cannot generate fallback image")
        return False
