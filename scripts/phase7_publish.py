#!/usr/bin/env python3
"""
Phase 7: Post final game listing + promo image to Telegram channel.
Update portfolio website.
"""

import sys
import os
import json
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from scripts.utils import send_to_channel, send_to_admin, get_current_game, mark_game_completed, load_json, generate_image

def generate_promo_image(genre, game_url):
    """Generate a promotional image for the channel."""
    prompt = f"Promotional banner for '{genre}' mobile game, vibrant, with text 'Deathroll Studio'"
    out_path = os.path.join(config.OUTPUT_DIR, f"promo_{genre}.png")
    generate_image(prompt, out_path, width=800, height=400)
    return out_path

def post_to_channel(genre, game_url, promo_path):
    """Send game listing to @drolltech channel."""
    caption = f"""🎮 *New Game Released by Deathroll Studio*

Genre: {genre}
Play now (installable PWA): {game_url}

#DeathrollFactory #{genre.replace(' ', '')} #MobileGame
"""
    # Send photo with caption
    from scripts.utils import send_telegram
    # We need to send photo, but our send_telegram only does text. Let's add a quick photo sender.
    url = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/sendPhoto"
    with open(promo_path, "rb") as photo:
        files = {"photo": photo}
        data = {"chat_id": config.TELEGRAM_CHANNEL_ID, "caption": caption, "parse_mode": "Markdown"}
        response = requests.post(url, files=files, data=data)
    return response.ok

def update_portfolio_website(game_url, genre):
    """Simple static portfolio: append to index.html in docs/"""
    portfolio_index = os.path.join(config.BASE_DIR, "docs", "index.html")
    if not os.path.exists(portfolio_index):
        # Create basic portfolio
        with open(portfolio_index, "w") as f:
            f.write("<html><body><h1>Deathroll Studio Games</h1><ul></ul></body></html>")
    with open(portfolio_index, "r") as f:
        content = f.read()
    # Insert new game
    new_entry = f'<li><a href="{game_url}">{genre}</a></li>'
    if new_entry not in content:
        content = content.replace("</ul>", f"{new_entry}</ul>")
        with open(portfolio_index, "w") as f:
            f.write(content)

def main():
    game, _ = get_current_game()
    if not game:
        send_to_admin("No active game for Phase 7.")
        return
    genre = game["genre"]
    send_to_admin(f"📢 *Phase 7 Started*: Publishing {genre}")
    
    state = load_json(config.RUN_STATE_FILE)
    game_url = state.get("phase_data", {}).get("game_url")
    if not game_url:
        game_url = f"https://{os.getenv('GITHUB_REPOSITORY_OWNER', 'user')}.github.io/deathroll-factory/{genre.replace(' ', '_')}/"
    
    promo_path = generate_promo_image(genre, game_url)
    success = post_to_channel(genre, game_url, promo_path)
    if success:
        send_to_admin(f"✅ Posted to channel @drolltech")
    else:
        send_to_admin(f"⚠️ Failed to post to channel, but game is ready.")
    
    update_portfolio_website(game_url, genre)
    mark_game_completed(genre, game_url, promo_path)
    
    send_to_admin(f"🎉 Game '{genre}' COMPLETE! Check {game_url}")
    # Reset phase state for next game
    set_phase_state(1, {})

if __name__ == "__main__":
    main()
