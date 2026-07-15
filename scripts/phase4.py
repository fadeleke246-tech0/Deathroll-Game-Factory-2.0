#!/usr/bin/env python3
import re
import sys
import time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts import config
from scripts import utils
from scripts.memory import memory

def build_advanced_prompt(asset: str, game: dict) -> str:
    genre = game['genre']
    title = game['title']
    concept = game['concept']
    mood = "dark and gritty" if "war" in genre or "shooter" in genre else "bright and colorful"
    style = "pixel art" if genre in ["platformer", "puzzle"] else "photorealistic, 4K"
    if asset == "background":
        return f"{title} game {genre} background, {mood}, {style}, highly detailed, concept art"
    elif asset == "player":
        return f"Main character for {title}, {genre} game, {mood}, {style}, full body, dynamic pose"
    elif asset == "enemy":
        return f"Enemy for {title}, {genre} game, {mood}, {style}, menacing, detailed"
    elif asset == "bullet":
        return f"Projectile for {title}, {genre} game, glowing, {style}"
    else:
        return f"Game art for {title}, {asset}, {mood}, {style}"

def main():
    print("🎨 PHASE 4: ART (advanced prompts)")
    state = utils.load_json(config.DATA_DIR / "run_state.json")
    if state.get("phase") != 4:
        print(f"Expected phase 4, got {state.get('phase')}. Skipping.")
        return

    game = state["current_game"]
    utils.send_telegram_admin(f"🎨 Phase 4 started: generating advanced images for '{game['title']}'...")

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
        prompt = build_advanced_prompt(asset, game)
        out = assets_dir / f"{asset}.png"
        utils.send_telegram_admin(f"🎨 Generating {asset} with prompt: {prompt[:80]}...")
        success = utils.generate_image(prompt, out)
        if success:
            utils.send_telegram_admin(f"✅ {asset} done")
        else:
            utils.send_telegram_admin(f"❌ {asset} failed, fallback used")
        time.sleep(1)

    # Promo image
    promo_path = config.DOCS_DIR / f"promo_{game['id']}.png"
    promo_prompt = f"Promotional banner for {game['title']}, {game['genre']} game, eye-catching, vibrant"
    utils.generate_image(promo_prompt, promo_path)
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
