#!/usr/bin/env python3
"""
Phase 1: Research current genre using Gemini.
Sends report to admin DM, waits for /approve or auto-approves after 1 hour.
"""

import sys
import os
import time
import json
import requests

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from scripts.utils import (
    send_to_admin, get_current_game, update_game_status,
    get_phase_state, set_phase_state, load_json, save_json
)

# Gemini API endpoint
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={config.GEMINI_API_KEY}"

def call_gemini(prompt):
    """Send prompt to Gemini, return text response."""
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    try:
        r = requests.post(GEMINI_URL, json=payload, timeout=60)
        r.raise_for_status()
        data = r.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return f"Gemini error: {e}"

def research_genre(genre):
    """Research a specific genre and return report text."""
    prompt = f"""You are a game design researcher. Analyze the genre "{genre}" for a small offline HTML5 mobile game.

Answer in this exact format:
COST_FEASIBILITY: (Low/Medium/High) - with brief reason
KEY_MECHANICS: bullet list of 3-5 core loops
ASSETS_NEEDED: list all asset types (sprites, sounds, UI)
TECHNICAL_NOTES: any canvas/web-specific advice
ESTIMATED_DEV_TIME: in hours (greybox + art + polish)
SAMPLE_GAME_IDEAS: 2 concrete mini-game concepts with names

Keep total under 800 words.
"""
    return call_gemini(prompt)

def wait_for_approval(genre):
    """Poll Telegram for /approve command or auto-approve after 1 hour."""
    send_to_admin(f"📊 *Phase 1 Report for {genre}*\nWaiting for /approve or auto-approve in {config.AUTO_APPROVE_WAIT_MINUTES} minutes.")
    start = time.time()
    last_update_id = 0
    # We'll simulate by checking a simple file flag or env var.
    # For simplicity, we'll create a temp approval file.
    approval_file = os.path.join(config.DATA_DIR, f"approve_{genre}.txt")
    if os.path.exists(approval_file):
        os.remove(approval_file)
    
    while time.time() - start < config.AUTO_APPROVE_WAIT_MINUTES * 60:
        # Fetch updates from Telegram
        url = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/getUpdates"
        try:
            resp = requests.get(url, params={"offset": last_update_id + 1, "timeout": 30})
            updates = resp.json().get("result", [])
            for upd in updates:
                last_update_id = upd["update_id"]
                if "message" in upd and "text" in upd["message"]:
                    text = upd["message"]["text"].strip().lower()
                    if text == "/approve":
                        send_to_admin("✅ Approved! Moving to Phase 2.")
                        return True
        except:
            pass
        time.sleep(10)
    # Auto-approve
    send_to_admin("⏰ Auto-approval timeout reached. Moving to Phase 2.")
    return True

def main():
    game, idx = get_current_game()
    if not game:
        send_to_admin("No pending game in queue. Exiting Phase 1.")
        return
    
    genre = game["genre"]
    send_to_admin(f"🔍 *Phase 1 Started*: Researching genre '{genre}'")
    
    report = research_genre(genre)
    # Save report for later phases
    sar_data = {
        "genre": genre,
        "report": report,
        "timestamp": time.time()
    }
    save_json(config.SAR_FILE, sar_data)
    
    # Send report to admin
    msg = f"📖 *Research Report – {genre}*\n\n{report[:3800]}"  # Telegram limit 4096
    send_to_admin(msg)
    
    # Wait for approval
    approved = wait_for_approval(genre)
    if approved:
        update_game_status(genre, "phase1_done")
        set_phase_state(2, {"genre": genre, "research_report": report})
        send_to_admin(f"✅ Phase 1 complete for {genre}. Ready for Phase 2.")
    else:
        send_to_admin(f"❌ Phase 1 not approved. Check manually.")

if __name__ == "__main__":
    main()
