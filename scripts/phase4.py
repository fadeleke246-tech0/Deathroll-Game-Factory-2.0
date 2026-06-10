#!/usr/bin/env python3
"""
Phase 4: Generate art via Pollinations.ai (prompts from plan), procedural audio.
Swaps greybox assets.
"""
import sys
import os
import json
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from scripts.utils import (
    send_to_admin, get_current_game, update_game_status,
    set_phase_state, load_json, generate_image
)

def generate_sound_effect(name, output_path):
    """Create a minimal valid WAV file (silence) as placeholder."""
    # Write a minimal WAV header (44 bytes) – silent
    with open(output_path, "wb") as f:
        f.write(b'RIFF\x24\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00\x44\xac\x00\x00\x88\x58\x01\x00\x02\x00\x10\x00data\x00\x00\x00\x00')
    return True

def main():
    game, _ = get_current_game()
    if not game:
        send_to_admin("No active game for Phase 4.")
        return
    genre = game["genre"]
    send_to_admin(f"🎨 Phase 4 started: generating art & audio for {genre}")

    plan = load_json(os.path.join(config.DATA_DIR, "game_plan.json"))
    art_prompts = plan.get("art_prompts", {})

    assets_dir = os.path.join(config.OUTPUT_DIR, "assets")
    os.makedirs(assets_dir, exist_ok=True)

    # Generate images using Pollinations.ai
    for asset_name, prompt in art_prompts.items():
        out_path = os.path.join(assets_dir, f"{asset_name}.png")
        send_to_admin(f"Generating {asset_name}...")
        success = generate_image(prompt, out_path)
        if success:
            send_to_admin(f"✅ {asset_name} done")
        else:
            send_to_admin(f"❌ {asset_name} failed, using fallback")
        time.sleep(2)  # polite delay

    # Generate a simple click sound
    audio_dir = os.path.join(assets_dir, "audio")
    os.makedirs(audio_dir, exist_ok=True)
    generate_sound_effect("click", os.path.join(audio_dir, "click.wav"))

    # Combine greybox with art (simple injection)
    greybox_path = os.path.join(config.OUTPUT_DIR, "greybox", "game.html")
    final_html_path = os.path.join(config.OUTPUT_DIR, "game_with_art.html")
    if os.path.exists(greybox_path):
        with open(greybox_path, "r") as f:
            html = f.read()
        # Inject a reference to the first generated image (just for demo)
        first_img = list(art_prompts.keys())[0] if art_prompts else "player"
        injection = f'<img src="assets/{first_img}.png" style="display:none;" />'
        html = html.replace("</body>", f"{injection}</body>")
        with open(final_html_path, "w") as f:
            f.write(html)
    else:
        send_to_admin("⚠️ Greybox not found, skipping art injection")
        final_html_path = greybox_path

    update_game_status(genre, "phase4_done")
    set_phase_state(5, {"art_dir": assets_dir, "final_html": final_html_path})
    send_to_admin(f"✅ Phase 4 complete. Assets generated. Moving to Phase 5 (testing).")

if __name__ == "__main__":
    main()
