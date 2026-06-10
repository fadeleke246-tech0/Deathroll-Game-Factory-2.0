#!/usr/bin/env python3
"""
Phase 3: Build grey-box HTML5 game with basic logic (no art).
Output: output/greybox/game.html
"""

import sys
import os
import json
import shutil

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from scripts.utils import send_to_admin, get_current_game, update_game_status, load_json

TEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <title>{title}</title>
    <style>
        body {{ margin: 0; padding: 0; overflow: hidden; touch-action: none; background: #222; }}
        canvas {{ display: block; margin: auto; background: #333; }}
        #info {{ position: absolute; top: 10px; left: 10px; color: white; font-family: monospace; }}
    </style>
</head>
<body>
    <div id="info">Greybox: {genre} | Score: <span id="score">0</span></div>
    <canvas id="gameCanvas" width="{width}" height="{height}"></canvas>
    <script>
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');
        const scoreSpan = document.getElementById('score');
        let score = 0;
        
        // Simple placeholder mechanics for {genre}
        let player = {{ x: canvas.width/2, y: canvas.height-50, size: 30 }};
        let obstacles = [];
        
        function update() {{
            // Add placeholder logic here (movement, collisions)
            ctx.fillStyle = '#444';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = '#0f0';
            ctx.fillRect(player.x - player.size/2, player.y - player.size/2, player.size, player.size);
            ctx.fillStyle = '#f00';
            for(let obs of obstacles) {{
                ctx.fillRect(obs.x, obs.y, 20, 20);
            }}
            requestAnimationFrame(update);
        }}
        
        // Touch/mouse controls
        canvas.addEventListener('touchmove', (e) => {{
            e.preventDefault();
            let rect = canvas.getBoundingClientRect();
            let touchX = (e.touches[0].clientX - rect.left) * (canvas.width/rect.width);
            player.x = Math.min(Math.max(touchX, 20), canvas.width-20);
        }});
        canvas.addEventListener('mousemove', (e) => {{
            let rect = canvas.getBoundingClientRect();
            let mouseX = (e.clientX - rect.left) * (canvas.width/rect.width);
            player.x = Math.min(Math.max(mouseX, 20), canvas.width-20);
        }});
        
        update();
    </script>
</body>
</html>"""

def build_greybox(genre):
    width, height = 400, 600
    title = f"Deathroll Studio - {genre} (Greybox)"
    html = TEMPLATE.format(title=title, genre=genre, width=width, height=height)
    
    out_dir = os.path.join(config.OUTPUT_DIR, "greybox")
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "game.html")
    with open(out_file, "w") as f:
        f.write(html)
    return out_file

def main():
    game, _ = get_current_game()
    if not game:
        send_to_admin("No active game for Phase 3.")
        return
    genre = game["genre"]
    send_to_admin(f"🛠️ *Phase 3 Started*: Building greybox for {genre}")
    
    greybox_path = build_greybox(genre)
    update_game_status(genre, "phase3_done")
    set_phase_state(4, {"greybox_path": greybox_path})
    send_to_admin(f"✅ Greybox ready: {greybox_path}. Moving to Phase 4 (Art & Audio).")

if __name__ == "__main__":
    main()
