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
    set_phase_state, save_json
)

# Use a currently supported stable model
GEMINI_MODEL = "gemini-2.5-flash"
# Use the v1beta endpoint with header auth (more modern)
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"

def call_gemini(prompt):
    """Send prompt to Gemini, return text response."""
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": config.GEMINI_API_KEY  # Use header instead of URL param
    }
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    try:
        r = requests.post(GEMINI_URL, headers=headers, json=payload, timeout=60)
        if r.status_code != 200:
            return f"HTTP {r.status_code}: {r.text[:200]}"
        data = r.json()
        # Safely extract the generated text
        try:
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError):
            return f"Unexpected API response structure: {data}"
    except Exception as e:
        return f"Gemini error: {e}"

def research_genre(genre):
    prompt = f"""Analyze the genre "{genre}" for a small offline HTML5 mobile game.

Return in this exact format:
COST_FEASIBILITY: (Low/Medium/High) - reason
KEY_MECHANICS: bullet list
ASSETS_NEEDED: list
TECHNICAL_NOTES: advice
ESTIMATED_DEV_TIME: hours
SAMPLE_GAME_IDEAS: 2 concepts

Keep under 800 words."""
    return call_gemini(prompt)

def wait_for_approval(genre):
    start = time.time()
    last_update_id = 0
    # Use config.AUTO_APPROVE_WAIT_MINUTES from your config file (default 60)
    auto_approve_minutes = getattr(config, 'AUTO_APPROVE_WAIT_MINUTES', 60)
    send_to_admin(f"📊 *Phase 1 Report for {genre}*\nWaiting for /approve or auto-approve in {auto_approve_minutes} minutes.")
    
    while time.time() - start < auto_approve_minutes * 60:
        url = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/getUpdates"
        try:
            resp = requests.get(url, params={"offset": last_update_id + 1, "timeout": 30})
            updates = resp.json().get("result", [])
            for upd in updates:
                last_update_id = upd["update_id"]
                if "message" in upd and "text" in upd["message"]:
                    if upd["message"]["text"].strip().lower() == "/approve":
                        send_to_admin("✅ Approved! Moving to Phase 2.")
                        return True
        except Exception as e:
            print(f"Telegram polling error: {e}")
        time.sleep(10)
    send_to_admin("⏰ Auto-approval reached. Moving to Phase 2.")
    return True

def main():
    game, _ = get_current_game()
    if not game:
        send_to_admin("No pending game. Exiting Phase 1.")
        return
    genre = game["genre"]
    send_to_admin(f"🔍 Phase 1 started: researching '{genre}' using {GEMINI_MODEL}")
    report = research_genre(genre)
    save_json(config.SAR_FILE, {"genre": genre, "report": report, "timestamp": time.time()})
    send_to_admin(f"📖 Research report for {genre}:\n\n{report[:3500]}\n\nReply /approve to continue")
    approved = wait_for_approval(genre)
    if approved:
        update_game_status(genre, "phase1_done")
        set_phase_state(2, {"genre": genre, "research_report": report})
        send_to_admin(f"✅ Phase 1 complete for {genre}.")
    else:
        send_to_admin("Phase 1 not approved. Check manually.")

if __name__ == "__main__":
    main()
