#!/usr/bin/env python3
"""
Phase 4: Generate art assets required by the chosen template.
"""
import sys
import os
import time
import json
import shutil

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from scripts.utils import (
    send_to_admin, get_current_game, update_game_status,
    set_phase_state, load_json, generate_image
)

def main():
    game, _ = get_current_game()
    if not game:
        send_to_admin("No active game for Phase 4.")
        return
    genre = game["genre"]
    send_to_admin(f"🎨 Phase 4 started: generating art for {genre}")

    # 1. Get required asset names from current_assets.json
    assets_needed = ["player", "background"]
    assets_json_path = os.path.join(config.DATA_DIR, "current_assets.json")
    if os.path.exists(assets_json_path):
        with open(assets_json_path) as f:
            data = json.load(f)
            assets_needed = data.get("assets", assets_needed)
        send_to_admin(f"📋 Required assets: {', '.join(assets_needed)}")
    else:
        send_to_admin("⚠️ current_assets.json not found, using default asset list")

    # 2. Load plan to get art prompts
    plan = load_json(os.path.join(config.DATA_DIR, "game_plan.json"))
    art_prompts = plan.get("art_prompts", {})
    game_title = plan.get("game_title", genre)

    assets_dir = os.path.join(config.OUTPUT_DIR, "assets")
    os.makedirs(assets_dir, exist_ok=True)

    # 3. Generate each image
    for asset in assets_needed:
        prompt = art_prompts.get(asset, f"Game art for {asset}, {game_title}, {genre} style, pixel art, mobile game, simple shapes, vibrant")
        out_path = os.path.join(assets_dir, f"{asset}.png")
        send_to_admin(f"🎨 Generating {asset}...")
        success = generate_image(prompt, out_path)
        if success:
            send_to_admin(f"✅ {asset} done")
        else:
            send_to_admin(f"❌ {asset} failed, using fallback image")
        time.sleep(2)

    # 4. Copy greybox to final location
    greybox_path = os.path.join(config.OUTPUT_DIR, "greybox", "game.html")
    final_html_path = os.path.join(config.OUTPUT_DIR, "game_with_art.html")
    if os.path.exists(greybox_path):
        shutil.copy(greybox_path, final_html_path)
        send_to_admin("✅ Game HTML updated with art references")
    else:
        send_to_admin("⚠️ Greybox not found")
        final_html_path = greybox_path

    update_game_status(genre, "phase4_done")
    set_phase_state(5, {"art_dir": assets_dir, "final_html": final_html_path})
    send_to_admin("✅ Phase 4 complete. Moving to Phase 5 (testing).")

if __name__ == "__main__":
    main()
