#!/usr/bin/env python3
"""Phase 3: Build grey-box HTML5 prototype (no art)."""
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from scripts.utils import (
    send_to_admin, get_current_game, update_game_status,
    set_phase_state   # <-- MUST be present
)

GREYBOX_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <title>{title}</title>
    <style>body{{margin:0;overflow:hidden;background:#222;}} canvas{{display:block;margin:auto;background:#333;}}</style>
</head>
<body>
    <div style="position:absolute;top:10px;left:10px;color:white;">Score: <span id="score">0</span></div>
    <canvas id="gameCanvas" width="{width}" height="{height}"></canvas>
    <script>
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');
        let score = 0;
        let player = {{ x: canvas.width/2, y: canvas.height-50, size: 30 }};
        function update() {{
            ctx.fillStyle = '#444';
            ctx.fillRect(0,0,canvas.width,canvas.height);
            ctx.fillStyle = '#0f0';
            ctx.fillRect(player.x-player.size/2, player.y-player.size/2, player.size, player.size);
            requestAnimationFrame(update);
        }}
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

def main():
    game, _ = get_current_game()
    if not game:
        send_to_admin("No active game for Phase 3.")
        return
    genre = game["genre"]
    send_to_admin(f"🛠️ Phase 3 started: building greybox for {genre}")
    out_dir = os.path.join(config.OUTPUT_DIR, "greybox")
    os.makedirs(out_dir, exist_ok=True)
    html = GREYBOX_TEMPLATE.format(title=f"Deathroll - {genre}", width=400, height=600)
    greybox_path = os.path.join(out_dir, "game.html")
    with open(greybox_path, "w") as f:
        f.write(html)
    update_game_status(genre, "phase3_done")
    set_phase_state(4, {"greybox_path": greybox_path})
    send_to_admin("✅ Phase 3 complete. Moving to Phase 4 (art).")

if __name__ == "__main__":
    main()
