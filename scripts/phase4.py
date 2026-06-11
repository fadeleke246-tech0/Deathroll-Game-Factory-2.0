#!/usr/bin/env python3
import re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
import config
import utils

def extract_assets(html_path: Path) -> list:
    html = html_path.read_text()
    matches = re.findall(r'src="assets/([^"]+\.png)"', html)
    return list(set([m.split('.')[0] for m in matches]))

def main():
    print("🎨 PHASE 4: ART")
    state = utils.load_json(config.DATA_DIR / "run_state.json")
    game = state.get("current_game")
    if not game or game["phase"] != 4:
        print("No game in phase 4.")
        sys.exit(1)

    game_id = game["id"]
    game_dir = config.OUTPUT_DIR / game_id
    html_path = game_dir / "index.html"
    if not html_path.exists():
        print("index.html missing.")
        sys.exit(1)

    assets_needed = extract_assets(html_path)
    if not assets_needed:
        assets_needed = ["player", "enemy", "background", "bullet"]
    assets_dir = game_dir / "assets"
    assets_dir.mkdir(exist_ok=True)

    for asset in assets_needed:
        prompt = f"Game art for {game['title']}, {asset}, pixel art, mobile game style"
        out = assets_dir / f"{asset}.png"
        utils.generate_image(prompt, out)
        print(f"Generated {asset}.png")

    # Promo image
    promo = config.DOCS_DIR / f"promo_{game_id}.png"
    promo_prompt = f"Promotional banner for {game['title']}, mobile game"
    utils.generate_image(promo_prompt, promo)
    public_promo = f"{config.PUBLIC_BASE_URL}/promo_{game_id}.png"

    # Update portfolio
    portfolio = utils.load_json(config.DATA_DIR / "portfolio.json")
    portfolio[game_id] = {
        "title": game["title"],
        "genre": game["genre"],
        "concept": game["concept"],
        "promo": public_promo,
        "game_url": f"{config.PUBLIC_BASE_URL}/{game_id}/index.html",
    }
    utils.save_json(portfolio, config.DATA_DIR / "portfolio.json")

    state["phase"] = 5
    game["phase"] = 5
    utils.save_json(state, config.DATA_DIR / "run_state.json")
    print("✅ Phase 4 done. Moving to Phase 5 (Testing).")

if __name__ == "__main__":
    main()
