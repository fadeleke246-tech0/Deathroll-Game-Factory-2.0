#!/usr/bin/env python3
"""DUMMY Phase 1 – no API calls, just testing"""
import sys, os, time, json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from scripts.utils import send_to_admin, get_current_game, update_game_status, set_phase_state, save_json

def main():
    game, _ = get_current_game()
    if not game:
        send_to_admin("No pending game. Exiting.")
        return
    genre = game["genre"]
    send_to_admin(f"🧪 DUMMY Phase 1 started for {genre}")
    fake_report = f"This is a dummy research report for {genre}. No Gemini used."
    save_json(config.SAR_FILE, {"genre": genre, "report": fake_report, "timestamp": time.time()})
    send_to_admin(f"📖 Dummy report:\n{fake_report}\n\nAuto-approving in 5 seconds...")
    time.sleep(5)
    update_game_status(genre, "phase1_done")
    set_phase_state(2, {"genre": genre, "research_report": fake_report})
    send_to_admin("✅ Phase 1 (dummy) complete. Moving to Phase 2.")

if __name__ == "__main__":
    main()
