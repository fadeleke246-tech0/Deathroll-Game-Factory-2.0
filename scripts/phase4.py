#!/usr/bin/env python3
"""
Phase 4: Art & Audio
- Scans the generated game HTML for image references.
- Generates those images using Pollinations.ai (fallback to PIL).
- Generates a promo image for the storefront.
- Updates portfolio.json and games_queue.json with the image URLs.
"""
import sys
import re
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
import config
import utils


def extract_image_filenames(html_content: str) -> list:
    """
    Find all image filenames referenced in the HTML.
    Looks for src="assets/xxx.png" or similar.
    Returns list of unique names (without extension).
    """
    pattern = r'src="assets/([^"]+\.(png|jpg|jpeg))"'
    matches = re.findall(pattern, html_content, re.IGNORECASE)
    # Return base names without extension
    filenames = list(set([Path(m[0]).stem for m in matches]))
    print(f"📷 Found image references: {filenames}")
    return filenames


def main():
    print("🎨 PHASE 4: ART & AUDIO")

    state = utils.load_json(config.DATA_DIR / "run_state.json")
    game = state.get("current_game")
    if not game or game["phase"] != 4:
        print("❌ No game in art phase.")
        sys.exit(1)

    game_id = game["id"]
    game_output_dir = config.OUTPUT_DIR / game_id
    index_html_path = game_output_dir / "index.html"

    if not index_html_path.exists():
        print(f"❌ index.html not found at {index_html_path}")
        sys.exit(1)

    # 1. Read the generated HTML and extract required image filenames
    html_content = index_html_path.read_text(encoding="utf-8")
    required_images = extract_image_filenames(html_content)

    # 2. Generate each image using the plan's prompts (if available) or fallback prompts
    plan = utils.load_json(game_output_dir / "game_plan.json")
    art_prompts = plan.get("art_prompts", {})

    assets_dir = game_output_dir / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)

    for img_name in required_images:
        # Use a prompt from the plan if it exists, otherwise generate a generic prompt
        prompt = art_prompts.get(img_name, f"Game art for {game['title']}, {img_name}, pixel art style, simple and colourful")
        out_path = assets_dir / f"{img_name}.png"
        print(f"🎨 Generating {img_name}.png ...")
        if utils.generate_image(prompt, out_path):
            print(f"✅ Generated {img_name}.png")
        else:
            print(f"⚠️ Fallback image used for {img_name}")

    # 3. Generate a promo image for the storefront
    promo_prompt = f"Promotional image for a mobile game titled '{game['title']}'. {game['concept']}."
    promo_local_path = config.DOCS_DIR / f"promo_{game_id}.png"
    if utils.generate_image(promo_prompt, promo_local_path):
        public_promo_url = f"{config.PUBLIC_BASE_URL}/promo_{game_id}.png"
        print(f"✅ Promo image saved to {public_promo_url}")
    else:
        public_promo_url = ""   # fallback handled by storefront

    # 4. Update portfolio.json
    portfolio = utils.load_json(config.DATA_DIR / "portfolio.json")
    portfolio[game_id] = {
        "title": game["title"],
        "genre": game["genre"],
        "concept": game["concept"],
        "inspiration": game.get("inspiration", ""),
        "promo": public_promo_url,
        "game_url": f"{config.PUBLIC_BASE_URL}/{game_id}/index.html",
        "status": "art_done"
    }
    utils.save_json(portfolio, config.DATA_DIR / "portfolio.json")

    # 5. Update games_queue.json
    queue = utils.load_json(config.DATA_DIR / "games_queue.json")
    if game_id in queue:
        queue[game_id]["promo_image"] = public_promo_url
        queue[game_id]["status"] = "art_done"
        utils.save_json(queue, config.DATA_DIR / "games_queue.json")

    # 6. Advance to Phase 5 (Testing)
    state["phase"] = 5
    game["phase"] = 5
    game["status"] = "testing"
    utils.save_json(state, config.DATA_DIR / "run_state.json")

    print("✅ Phase 4 complete. Moving to Phase 5 (Testing).")


if __name__ == "__main__":
    main()
