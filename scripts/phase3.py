#!/usr/bin/env python3
"""
Phase 3: Greybox
- Selects a template based on genre.
- Injects the game plan into the template to produce a playable HTML file.
- Saves the greybox to output/<game_id>/index.html
"""

import sys
import shutil
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
import config
import utils


def select_template(genre: str) -> Path:
    """Return the path to the template HTML file for the given genre."""
    template_map = {
        "shooter": "shooter_template.html",
        "soccer": "soccer_template.html",
        "racing": "racing_template.html",
        "platformer": "platformer_template.html",
        "puzzle": "puzzle_template.html",
        "rpg": "rpg_template.html"
    }
    template_file = template_map.get(genre, "generic_template.html")
    return config.TEMPLATES_DIR / template_file


def inject_plan_into_template(template_path: Path, plan: dict, output_path: Path):
    """
    Very simple injection: replace placeholders like {{MECHANICS}} with plan values.
    In a real implementation, you might use a proper templating engine.
    """
    with open(template_path, "r", encoding="utf-8") as f:
        html = f.read()

    # Replace basic placeholders
    html = html.replace("{{TITLE}}", plan.get("title", "Game"))
    html = html.replace("{{MECHANICS}}", plan.get("mechanics", ""))
    html = html.replace("{{CONTROLS}}", plan.get("controls", ""))
    html = html.replace("{{VICTORY}}", plan.get("victory_condition", ""))

    # Write the greybox HTML
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"🎮 Greybox HTML written to {output_path}")


def main():
    print("📦 PHASE 3: GREYBOX")

    state = utils.load_json(config.DATA_DIR / "run_state.json")
    game = state.get("current_game")
    if not game or game["phase"] != 3:
        print("❌ No game in greybox phase.")
        sys.exit(1)

    game_id = game["id"]
    game_output_dir = config.OUTPUT_DIR / game_id
    plan_path = game_output_dir / "game_plan.json"

    if not plan_path.exists():
        print(f"❌ Plan not found at {plan_path}")
        sys.exit(1)

    plan = utils.load_json(plan_path)
    plan["title"] = game["title"]  # ensure title is present

    # Select and copy template
    template_path = select_template(game["genre"])
    if not template_path.exists():
        print(f"❌ Template missing: {template_path}. Using generic fallback.")
        template_path = config.TEMPLATES_DIR / "generic_template.html"

    output_html = game_output_dir / "index.html"
    inject_plan_into_template(template_path, plan, output_html)

    # Update state
    state["phase"] = 4
    game["phase"] = 4
    game["status"] = "art"
    utils.save_json(state, config.DATA_DIR / "run_state.json")

    print("✅ Phase 3 complete. Moving to Phase 4 (Art & Audio).")


if __name__ == "__main__":
    main()
