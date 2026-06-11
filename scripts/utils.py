"""
Utility functions used across all phases: JSON handling, image generation,
text extraction, Git operations, and Telegram messaging.
"""

import json
import re
import time
import shutil
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Any, Union

import requests
from PIL import Image, ImageDraw, ImageFont


# ----- File I/O -------------------------------------------------
def load_json(file_path: Path) -> Dict:
    """Load JSON from a file. Return empty dict if file missing or invalid."""
    if not file_path.exists():
        return {}
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        print(f"⚠️ Failed to load {file_path}: {e}")
        return {}


def save_json(data: Any, file_path: Path, indent: int = 2) -> bool:
    """Save data as JSON to a file. Returns True on success."""
    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=indent)
        return True
    except OSError as e:
        print(f"❌ Failed to save {file_path}: {e}")
        return False


# ----- LLM Response Parsing ------------------------------------
def extract_json_from_text(text: str) -> Optional[Dict]:
    """
    Extract JSON from LLM responses that may contain markdown or extra text.
    Handles ```json blocks or raw JSON objects.
    """
    # Try to find a ```json ... ``` block first
    match = re.search(r"```json\s*(\{.*?\})\s*```", text, re.DOTALL)
    if match:
        text = match.group(1)
    else:
        # Fallback: find the first { and last }
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1:
            text = text[start:end+1]
        else:
            return None
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        print(f"⚠️ JSON decode error: {e}")
        return None


# ----- Image Generation -----------------------------------------
def generate_image(prompt: str, output_path: Path) -> bool:
    """
    Generate an image using Pollinations.ai.
    Falls back to a coloured placeholder if the API fails.
    Returns True if an image exists at output_path.
    """
    try:
        encoded = requests.utils.quote(prompt)
        url = f"https://image.pollinations.ai/prompt/{encoded}?width=1024&height=1024"
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "wb") as f:
                f.write(response.content)
            print(f"✅ Generated image: {output_path}")
            return True
    except Exception as e:
        print(f"⚠️ Pollinations.ai failed: {e}")

    # Fallback: create a simple coloured image with text
    try:
        img = Image.new("RGB", (512, 512), color="#2c3e50")
        draw = ImageDraw.Draw(img)
        # Use default PIL font (no external font needed)
        draw.text((256, 256), prompt[:50], fill="white", anchor="mm")
        img.save(output_path)
        print(f"🎨 Created fallback image: {output_path}")
        return True
    except Exception as e:
        print(f"❌ Fallback image creation failed: {e}")
        return False


# ----- Git Operations -------------------------------------------
def commit_and_push(message: str, paths: List[str]) -> bool:
    """
    Add, commit, and push changes using git.
    Returns True if all commands succeed.
    """
    try:
        subprocess.run(["git", "add"] + paths, check=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", message], check=True, capture_output=True)
        subprocess.run(["git", "push"], check=True, capture_output=True)
        print(f"✅ Committed and pushed: {message}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Git operation failed: {e.stderr.decode() if e.stderr else e}")
        return False


def copy_game_to_docs(game_id: str, output_dir: Path, docs_dir: Path) -> bool:
    """
    Copy all game files from output_dir/game_id to docs_dir/game_id.
    Ensures the main HTML is named index.html.
    """
    source = output_dir / game_id
    dest = docs_dir / game_id
    if not source.exists():
        print(f"❌ Source game folder missing: {source}")
        return False

    # Remove old destination if exists
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True, exist_ok=True)

    # Copy all files
    for item in source.iterdir():
        if item.is_file():
            shutil.copy2(item, dest / item.name)

    # Rename main HTML to index.html if needed
    # Assumes the game entry point is either index.html or game.html
    index_candidates = ["index.html", "game.html", f"{game_id}.html"]
    for candidate in index_candidates:
        candidate_path = dest / candidate
        if candidate_path.exists() and candidate != "index.html":
            candidate_path.rename(dest / "index.html")
            break

    print(f"📦 Copied game '{game_id}' to {dest}")
    return True


# ----- Telegram -------------------------------------------------
def send_telegram_message(bot_token: str, channel: str, message: str) -> bool:
    """Send a plain text message to a Telegram channel."""
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": channel, "text": message, "parse_mode": "Markdown"}
    try:
        resp = requests.post(url, json=payload, timeout=10)
        if resp.status_code == 200:
            print("✅ Telegram message sent")
            return True
        else:
            print(f"⚠️ Telegram error: {resp.text}")
            return False
    except Exception as e:
        print(f"❌ Telegram send failed: {e}")
        return False
