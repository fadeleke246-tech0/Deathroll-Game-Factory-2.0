#!/usr/bin/env python3
import re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import config
import utils

def main():
    print("🎨 PHASE 4: ART")
    state = utils.load_json(config.DATA_DIR / "run_state.json")
    if state.get("phase") != 4:
        print(f"Expected phase 4, got {state.get('phase')}. Skipping.")
        return

    game = state["current_game"]
    utils.send_telegram_admin(f"🎨 Phase 4 started: generating images for '{game['title']}'...")

    game_dir = config.OUTPUT_DIR / game["id"]
    html_path = game_dir / "index.html"
    if not html_path.exists():
        utils.send_telegram_admin("❌ Phase 4 failed: index.html missing.")
        sys.exit(1)

    html = html_path.read_text()
    matches = re.findall(r'src="assets/([^"]+\.png)"', html)
    assets = list(set([m.split('.')[0] for m in matches]))
    if not assets:
        assets = ["player", "enemy", "background", "bullet"]

    assets_dir = game_dir / "assets"
    assets_dir.mkdir(exist_ok=True)
    for asset in assets:
        prompt = f"Game art for {game['title']}, {asset}, pixel art"
        out = assets_dir / f"{asset}.png"
        utils.generate_image(prompt, out)

    promo_path = config.DOCS_DIR / f"promo_{game['id']}.png"
    utils.generate_image(f"Promotional image for {game['title']}", promo_path)
    public_promo = f"{config.PUBLIC_BASE_URL}/promo_{game['id']}.png"

    portfolio = utils.load_json(config.DATA_DIR / "portfolio.json")
    portfolio[game["id"]] = {
        "title": game["title"],
        "genre": game["genre"],
        "concept": game["concept"],
        "promo": public_promo,
        "game_url": f"{config.PUBLIC_BASE_URL}/{game['id']}/index.html"
    }
    utils.save_json(portfolio, config.DATA_DIR / "portfolio.json")

    state["phase"] = 5
    utils.save_json(state, config.DATA_DIR / "run_state.json")
    utils.send_telegram_admin("✅ Phase 4 complete: art generated. Moving to Phase 5 tomorrow.")
    print("Phase 4 done. State advanced to phase 5.")

if __name__ == "__main__":
    main()
