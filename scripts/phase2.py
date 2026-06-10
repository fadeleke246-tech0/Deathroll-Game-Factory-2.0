#!/usr/bin/env python3
"""Phase 2: Generate game plan (architecture, asset list, art prompts)."""
import sys
import os
import json
import time
import requests

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from scripts.utils import send_to_admin, get_current_game, update_game_status, load_json, save_json, set_phase_state

# Use the same supported model as Phase 1
GEMINI_MODEL = "gemini-2.5-flash"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"

def call_gemini(prompt):
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": config.GEMINI_API_KEY
    }
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    try:
        r = requests.post(GEMINI_URL, headers=headers, json=payload, timeout=60)
        if r.status_code != 200:
            return f"HTTP {r.status_code}: {r.text[:200]}"
        data = r.json()
        try:
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError):
            return f"Unexpected API response structure: {data}"
    except Exception as e:
        return f"Gemini error: {e}"

def generate_plan(genre, research_report):
    prompt = f"""Based on this research:
{research_report}

Create a detailed game plan for a complete HTML5/JS mobile game. Output valid JSON only with these keys:
{{
  "architecture": "...",
  "asset_list": ["sprite1.png", ...],
  "art_prompts": {{"background":"prompt", "player":"prompt", "enemy":"prompt", "ui_button":"prompt"}},
  "dependency_map": {{"libraries":[], "external":[]}},
  "file_structure": {{"index.html":"main", "game.js":"logic", "style.css":"styles"}}
}}
No text outside JSON."""
    response = call_gemini(prompt)
    try:
        # Attempt to parse the response as JSON
        return json.loads(response)
    except json.JSONDecodeError:
        # Fallback plan if Gemini doesn't return valid JSON
        send_to_admin(f"⚠️ Gemini returned invalid JSON. Using fallback plan.\nResponse snippet: {response[:200]}")
        return {
            "architecture": "Standard requestAnimationFrame loop",
            "asset_list": ["player.png", "bg.png", "click.wav"],
            "art_prompts": {"player": f"pixel art {genre} character", "background": f"simple {genre} background"},
            "dependency_map": {"libraries": [], "external": []},
            "file_structure": {"index.html": "canvas", "game.js": "logic"}
        }

def main():
    game, _ = get_current_game()
    if not game:
        send_to_admin("No active game in Phase 2.")
        return
    genre = game["genre"]
    sar = load_json(config.SAR_FILE)
    research = sar.get("report", "")
    send_to_admin(f"📐 Phase 2 started: planning {genre}")
    plan = generate_plan(genre, research)
    plan_file = os.path.join(config.DATA_DIR, "game_plan.json")
    save_json(plan_file, plan)
    update_game_status(genre, "phase2_done")
    set_phase_state(3, {"plan": plan})
    send_to_admin("✅ Phase 2 complete. Moving to Phase 3.")

if __name__ == "__main__":
    main()
