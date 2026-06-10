#!/usr/bin/env python3
"""
Phase 6: Wrap game as PWA (manifest, service worker) and upload to GitHub Pages.
"""
import sys
import os
import shutil
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from scripts.utils import (
    send_to_admin, get_current_game, update_game_status,
    load_json, set_phase_state
)

def create_pwa_files(game_dir, game_title):
    manifest = {
        "name": game_title,
        "short_name": game_title[:12],
        "start_url": ".",
        "display": "standalone",
        "theme_color": "#000000",
        "background_color": "#ffffff",
        "icons": [
            {"src": "icon-192.png", "sizes": "192x192", "type": "image/png"}
        ]
    }
    with open(os.path.join(game_dir, "manifest.json"), "w") as f:
        json.dump(manifest, f)

    sw_js = """self.addEventListener('install', e => { e.waitUntil(self.skipWaiting()); });
self.addEventListener('fetch', e => { e.respondWith(fetch(e.request)); });"""
    with open(os.path.join(game_dir, "sw.js"), "w") as f:
        f.write(sw_js)

    # Generate dummy icon using PIL
    try:
        from PIL import Image, ImageDraw
        img = Image.new('RGB', (192,192), color='green')
        d = ImageDraw.Draw(img)
        d.text((10,80), "DS", fill='white')
        img.save(os.path.join(game_dir, "icon-192.png"))
    except ImportError:
        send_to_admin("⚠️ PIL not available, icon not created")

def main():
    game, _ = get_current_game()
    if not game:
        send_to_admin("No active game for Phase 6.")
        return
    genre = game["genre"]
    send_to_admin(f"📦 *Phase 6 Started*: Building PWA for {genre}")

    state = load_json(config.RUN_STATE_FILE)   # FIXED
    html_path = state.get("phase_data", {}).get("tested_html", os.path.join(config.OUTPUT_DIR, "game_with_art.html"))

    pages_dir = os.path.join(config.BASE_DIR, "docs")
    os.makedirs(pages_dir, exist_ok=True)
    game_slug = genre.replace(" ", "_")
    game_output_dir = os.path.join(pages_dir, game_slug)
    os.makedirs(game_output_dir, exist_ok=True)

    shutil.copy(html_path, os.path.join(game_output_dir, "index.html"))
    assets_src = os.path.join(config.OUTPUT_DIR, "assets")
    if os.path.exists(assets_src):
        shutil.copytree(assets_src, os.path.join(game_output_dir, "assets"), dirs_exist_ok=True)

    create_pwa_files(game_output_dir, f"Deathroll {genre}")

    owner = os.getenv("GITHUB_REPOSITORY_OWNER", "fadeleke246-tech0")
    repo = os.getenv("GITHUB_REPOSITORY", "Deathroll-Game-Factory-2.0").split("/")[-1]
    game_url = f"https://{owner}.github.io/{repo}/{game_slug}/"

    update_game_status(genre, "phase6_done", {"game_url": game_url})
    set_phase_state(7, {"game_url": game_url, "local_path": game_output_dir})
    send_to_admin(f"✅ PWA built at {game_url}. Moving to Phase 7.")

if __name__ == "__main__":
    main()
