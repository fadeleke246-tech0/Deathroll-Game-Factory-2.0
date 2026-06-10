#!/usr/bin/env python3
import sys, os, time, json, requests

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from scripts.utils import send_to_admin, get_current_game, update_game_status, set_phase_state, save_json

GEMINI_MODEL = "gemini-1.0-pro"   # More stable
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={config.GEMINI_API_KEY}"

def call_gemini(prompt):
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    try:
        r = requests.post(GEMINI_URL, json=payload, timeout=60)
        if r.status_code != 200:
            return f"HTTP {r.status_code}: {r.text[:200]}"
        data = r.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return f"Exception: {e}"

def research_genre(genre):
    prompt = f"Analyze genre '{genre}' for a small offline HTML5 mobile game. Return: COST_FEASIBILITY, KEY_MECHANICS, ASSETS_NEEDED, TECHNICAL_NOTES, ESTIMATED_DEV_TIME, SAMPLE_GAME_IDEAS. Keep under 800 words."
    return call_gemini(prompt)

def main():
    game, _ = get_current_game()
    if not game:
        send_to_admin("No pending game.")
        return
    genre = game["genre"]
    send_to_admin(f"Phase 1 started for {genre}")
    report = research_genre(genre)
    save_json(config.SAR_FILE, {"genre": genre, "report": report, "timestamp": time.time()})
    send_to_admin(f"Report:\n{report[:3000]}\n\nReply /approve to continue (auto in 60 min)")
    # Wait 60 seconds for demo, or longer? Use 60 seconds for test
    time.sleep(60)
    update_game_status(genre, "phase1_done")
    set_phase_state(2, {})
    send_to_admin("Phase 1 done, moving to Phase 2.")

if __name__ == "__main__":
    main()
