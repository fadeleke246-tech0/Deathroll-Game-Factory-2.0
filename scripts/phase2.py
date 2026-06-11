#!/usr/bin/env python3
"""Phase 2: Generate game plan (architecture, asset list, art prompts)."""
import sys
import os
import json
import time
import re
import requests

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from scripts.utils import send_to_admin, get_current_game, update_game_status, load_json, save_json, set_phase_state

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

def extract_json_from_text(text):
    """Extract the first valid JSON object from text (handles markdown, extra words)."""
    # Try to find JSON between triple backticks
    match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if match:
        json_str = match.group(1)
    else:
        # Find first { and last } in the string
        start = text.find('{')
        end = text.rfind('}')
        if start != -1 and end != -1 and end > start:
            json_str = text[start:end+1]
        else:
            return None
    # Parse JSON
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        send_to_admin(f"⚠️ JSON parse error: {e}\nAttempted string: {json_str[:200]}")
        return None

def generate_plan(genre, research_report):
    prompt = f"""Based on this research:
{research_report}

Create a detailed game plan for a complete HTML5/JS mobile game. Output **only** a valid JSON object with these keys:
{{
  "architecture": "...",
  "asset_list": ["sprite1.png", ...],
  "art_prompts": {{"background":"prompt", "player":"prompt", "enemy":"prompt", "ui_button":"prompt"}},
  "dependency_map": {{"libraries":[], "external":[]}},
  "file_structure": {{"index.html":"main", "game.js":"logic", "style.css":"styles"}}
}}
Do not include any other text, explanations, or markdown. Only the JSON."""
    response = call_gemini(prompt)
    send_to_admin(f"Raw Gemini response (first 300 chars):\n{response[:300]}")
    plan = extract_json_from_text(response)
    if plan is None:
        send_to_admin("⚠️ Failed to extract JSON. Using fallback plan.")
        return {
            "architecture": "Standard requestAnimationFrame loop",
            "asset_list": ["player.png", "bg.png", "click.wav"],
            "art_prompts": {"player": f"pixel art {genre} character", "background": f"simple {genre} background"},
            "dependency_map": {"libraries": [], "external": []},
            "file_structure": {"index.html": "canvas", "game.js": "logic"}
        }
    return plan

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
