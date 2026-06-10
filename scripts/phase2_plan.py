#!/usr/bin/env python3
"""DUMMY Phase 2 – creates a simple plan without Gemini"""
import sys, os, json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from scripts.utils import send_to_admin, get_current_game, update_game_status, save_json, set_phase_state

def main():
    game, _ = get_current_game()
    if not game:
        send_to_admin("No active game in Phase 2 (dummy).")
        return
    genre = game["genre"]
    send_to_admin(f"📐 DUMMY Phase 2 started for {genre}")
    plan = {
        "architecture": "Simple canvas loop",
        "asset_list": ["player.png", "bg.png"],
        "art_prompts": {"player": "pixel art character", "background": "simple background"},
        "dependency_map": {"libraries": []},
        "file_structure": {"index.html": "canvas", "game.js": "logic"}
    }
    plan_file = os.path.join(config.DATA_DIR, "game_plan.json")
    save_json(plan_file, plan)
    update_game_status(genre, "phase2_done")
    set_phase_state(3, {"plan": plan})
    send_to_admin("✅ Phase 2 (dummy) complete. Moving to Phase 3.")

if __name__ == "__main__":
    main()
