#!/usr/bin/env python3
"""
Phase 2: Generate game plan (architecture, asset list, prompts).
Output: data/game_plan.json
"""
import sys
import os
import json
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from scripts.utils import send_to_admin, get_current_game, update_game_status, load_json, save_json

# Reuse same Gemini call as phase1 (but we need to define it here or import)
# To avoid circular import, we'll define call_gemini again using same model
GEMINI_MODEL = "gemini-pro"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={config.GEMINI_API_KEY}"

def call_gemini(prompt):
    import requests
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    try:
        r = requests.post(GEMINI_URL, json=payload, timeout=60)
        r.raise_for_status()
        data = r.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return f"Gemini error: {e}"

def generate_plan(genre, research_report):
    prompt = f"""Based on this research:
{research_report}

Create a detailed game plan for a complete HTML5/JS mobile game. Output valid JSON only with these keys:
{{
  "architecture": "brief description of code structure (main loop, collision, etc.)",
  "asset_list": ["sprite1.png", "sound1.ogg", ...],
  "art_prompts": {{
    "background": "detailed prompt for Pollinations.ai",
    "player": "prompt",
    "enemy": "prompt",
    "ui_button": "prompt"
  }},
  "dependency_map": {{
    "libraries": ["none (vanilla JS)"],
    "external": []
  }},
  "file_structure": {{
    "index.html": "main entry",
    "game.js": "logic",
    "style.css": "styles"
  }}
}}
Do not include any text outside the JSON."""
    response = call_gemini(prompt)
    try:
        plan = json.loads(response)
    except:
        plan = {
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
    send_to_admin(f"📐 *Phase 2 Started*: Planning {genre}")
    plan = generate_plan(genre, research)
    plan_file = os.path.join(config.DATA_DIR, "game_plan.json")
    save_json(plan_file, plan)
    update_game_status(genre, "phase2_done")
    set_phase_state(3, {"plan": plan})
    send_to_admin(f"✅ Phase 2 complete. Plan saved. Moving to Phase 3.")

if __name__ == "__main__":
    main()
