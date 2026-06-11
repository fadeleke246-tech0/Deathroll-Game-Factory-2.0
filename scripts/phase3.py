#!/usr/bin/env python3
"""Phase 3: Auto‑create template folders and files, inject game title, copy to output."""
import sys
import os
import json
import shutil

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from scripts.utils import send_to_admin, get_current_game, update_game_status, set_phase_state, load_json

# ------------------------------------------------------------
# Embedded default templates for each genre category
# ------------------------------------------------------------
TEMPLATES = {
    "shooter": {
        "assets": ["player1", "player2", "background", "bullet"],
        "html": '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <title>{{TITLE}} – Deathroll Studio</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { background: #0a0a1a; display: flex; justify-content: center; align-items: center; min-height: 100vh; font-family: monospace; }
        canvas { border-radius: 12px; box-shadow: 0 0 20px rgba(0,0,0,0.5); cursor: crosshair; }
        .info { position: absolute; top: 10px; left: 10px; color: white; background: rgba(0,0,0,0.6); padding: 5px 12px; border-radius: 20px; }
    </style>
</head>
<body>
<div style="position: relative;">
    <canvas id="gameCanvas" width="800" height="600"></canvas>
    <div class="info">⚔️ LOCAL WARFARE | P1: WASD + left-click | P2: arrows + right-click</div>
</div>
<script>
    const canvas = document.getElementById('gameCanvas');
    const ctx = canvas.getContext('2d');
    
    let players = [
        { x: 200, y: 300, radius: 20, color: '#4caf50', health: 100, score: 0, keys: { w: false, s: false, a: false, d: false }, shooting: false, cooldown: 0 },
        { x: 600, y: 300, radius: 20, color: '#f44336', health: 100, score: 0, keys: { ArrowUp: false, ArrowDown: false, ArrowLeft: false, ArrowRight: false }, shooting: false, cooldown: 0 }
    ];
    let bullets = [];
    const bulletSpeed = 8;
    const playerSpeed = 5;
    
    let bgImg = new Image(); bgImg.src = "assets/background.png";
    let p1Img = new Image(); p1Img.src = "assets/player1.png";
    let p2Img = new Image(); p2Img.src = "assets/player2.png";
    let bulletImg = new Image(); bulletImg.src = "assets/bullet.png";
    
    window.addEventListener('keydown', (e) => {
        const key = e.key;
        if (key === 'w') players[0].keys.w = true;
        if (key === 's') players[0].keys.s = true;
        if (key === 'a') players[0].keys.a = true;
        if (key === 'd') players[0].keys.d = true;
        if (key === 'ArrowUp') players[1].keys.ArrowUp = true;
        if (key === 'ArrowDown') players[1].keys.ArrowDown = true;
        if (key === 'ArrowLeft') players[1].keys.ArrowLeft = true;
        if (key === 'ArrowRight') players[1].keys.ArrowRight = true;
        e.preventDefault();
    });
    window.addEventListener('keyup', (e) => {
        const key = e.key;
        if (key === 'w') players[0].keys.w = false;
        if (key === 's') players[0].keys.s = false;
        if (key === 'a') players[0].keys.a = false;
        if (key === 'd') players[0].keys.d = false;
        if (key === 'ArrowUp') players[1].keys.ArrowUp = false;
        if (key === 'ArrowDown') players[1].keys.ArrowDown = false;
        if (key === 'ArrowLeft') players[1].keys.ArrowLeft = false;
        if (key === 'ArrowRight') players[1].keys.ArrowRight = false;
    });
    canvas.addEventListener('mousedown', (e) => {
        if (e.button === 0) players[0].shooting = true;
        if (e.button === 2) players[1].shooting = true;
        e.preventDefault();
    });
    canvas.addEventListener('mouseup', (e) => {
        if (e.button === 0) players[0].shooting = false;
        if (e.button === 2) players[1].shooting = false;
    });
    canvas.addEventListener('contextmenu', (e) => e.preventDefault());
    
    function update() {
        for (let i=0; i<2; i++) {
            let p = players[i];
            if (i===0) {
                if (p.keys.w) p.y -= playerSpeed;
                if (p.keys.s) p.y += playerSpeed;
                if (p.keys.a) p.x -= playerSpeed;
                if (p.keys.d) p.x += playerSpeed;
            } else {
                if (p.keys.ArrowUp) p.y -= playerSpeed;
                if (p.keys.ArrowDown) p.y += playerSpeed;
                if (p.keys.ArrowLeft) p.x -= playerSpeed;
                if (p.keys.ArrowRight) p.x += playerSpeed;
            }
            p.x = Math.min(Math.max(p.x, p.radius), canvas.width - p.radius);
            p.y = Math.min(Math.max(p.y, p.radius), canvas.height - p.radius);
            if (p.cooldown > 0) p.cooldown--;
            if (p.shooting && p.cooldown === 0) {
                const rect = canvas.getBoundingClientRect();
                let mouseX = canvas.width/2, mouseY = canvas.height/2;
                if (window.event) {
                    mouseX = (window.event.clientX - rect.left) * (canvas.width/rect.width);
                    mouseY = (window.event.clientY - rect.top) * (canvas.height/rect.height);
                }
                let angle = Math.atan2(mouseY - p.y, mouseX - p.x);
                bullets.push({
                    x: p.x, y: p.y, radius: 5,
                    vx: Math.cos(angle) * bulletSpeed,
                    vy: Math.sin(angle) * bulletSpeed,
                    owner: i
                });
                p.cooldown = 15;
            }
        }
        for (let i=0; i<bullets.length; i++) {
            bullets[i].x += bullets[i].vx;
            bullets[i].y += bullets[i].vy;
            if (bullets[i].x < 0 || bullets[i].x > canvas.width || bullets[i].y < 0 || bullets[i].y > canvas.height) {
                bullets.splice(i,1);
                i--;
                continue;
            }
            for (let j=0; j<players.length; j++) {
                if (bullets[i].owner !== j) {
                    const dx = bullets[i].x - players[j].x;
                    const dy = bullets[i].y - players[j].y;
                    const dist = Math.sqrt(dx*dx + dy*dy);
                    if (dist < players[j].radius + bullets[i].radius) {
                        players[j].health -= 25;
                        bullets.splice(i,1);
                        i--;
                        if (players[j].health <= 0) {
                            players[j].health = 0;
                            players[1-j].score++;
                            players[j].health = 100;
                            players[j].x = (j===0?200:600);
                            players[j].y = 300;
                        }
                        break;
                    }
                }
            }
        }
    }
    function draw() {
        ctx.clearRect(0,0,canvas.width,canvas.height);
        if (bgImg.complete && bgImg.naturalWidth>0) ctx.drawImage(bgImg,0,0,canvas.width,canvas.height);
        else { ctx.fillStyle = '#2a2a3e'; ctx.fillRect(0,0,canvas.width,canvas.height); }
        for (let i=0;i<2;i++) {
            let p = players[i];
            let img = i===0 ? p1Img : p2Img;
            if (img.complete && img.naturalWidth>0) ctx.drawImage(img, p.x-p.radius, p.y-p.radius, p.radius*2, p.radius*2);
            else {
                ctx.beginPath();
                ctx.arc(p.x,p.y,p.radius,0,Math.PI*2);
                ctx.fillStyle = p.color;
                ctx.fill();
            }
            ctx.fillStyle = 'red';
            ctx.fillRect(p.x-p.radius, p.y-p.radius-10, p.radius*2, 5);
            ctx.fillStyle = 'lime';
            ctx.fillRect(p.x-p.radius, p.y-p.radius-10, (p.radius*2)*(p.health/100), 5);
            ctx.fillStyle = 'white';
            ctx.font = 'bold 16px monospace';
            ctx.fillText(`${p.score}`, p.x-8, p.y-15);
        }
        for (let b of bullets) {
            if (bulletImg.complete && bulletImg.naturalWidth>0) ctx.drawImage(bulletImg, b.x-4, b.y-4, 8, 8);
            else {
                ctx.fillStyle = 'yellow';
                ctx.beginPath();
                ctx.arc(b.x,b.y,4,0,Math.PI*2);
                ctx.fill();
            }
        }
        requestAnimationFrame(frame);
    }
    function frame() { update(); draw(); }
    frame();
</script>
</body>
</html>'''
    },
    "soccer": {
        "assets": ["ball", "goal", "field", "player"],
        "html": '''<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1,user-scalable=no"><title>{{TITLE}}</title><style>body{background:#0a0a1a;display:flex;justify-content:center;align-items:center;min-height:100vh;font-family:monospace;}</style></head><body><canvas id="gameCanvas" width="400" height="600"></canvas><script>
const canvas=document.getElementById('gameCanvas'),ctx=canvas.getContext('2d');
let score=0,power=0,shooting=false,angle=0,ball={x:200,y:500,r:10},goal={x:120,y:50,w:160,h:80};
let bgImg=new Image();bgImg.src="assets/field.png";
let ballImg=new Image();ballImg.src="assets/ball.png";
let goalImg=new Image();goalImg.src="assets/goal.png";
canvas.addEventListener('touchstart',()=>{shooting=true;});
canvas.addEventListener('touchend',()=>{if(shooting){let success=Math.random()<0.5;score+=success?1:0;shooting=false;}});
function draw(){
    ctx.clearRect(0,0,400,600);
    if(bgImg.complete&&bgImg.naturalWidth>0)ctx.drawImage(bgImg,0,0,400,600);
    if(goalImg.complete&&goalImg.naturalWidth>0)ctx.drawImage(goalImg,goal.x,goal.y,goal.w,goal.h);
    if(ballImg.complete&&ballImg.naturalWidth>0)ctx.drawImage(ballImg,ball.x-ball.r,ball.y-ball.r,ball.r*2,ball.r*2);
    else{ctx.fillStyle='white';ctx.beginPath();ctx.arc(ball.x,ball.y,ball.r,0,Math.PI*2);ctx.fill();}
    ctx.fillStyle='white';ctx.font='20px monospace';ctx.fillText('Score: '+score,10,50);
    requestAnimationFrame(draw);
}
draw();
</script></body></html>'''
    },
    "racing": {
        "assets": ["car", "road", "obstacle"],
        "html": '''<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1,user-scalable=no"><title>{{TITLE}}</title><style>body{background:#0a0a1a;display:flex;justify-content:center;align-items:center;min-height:100vh;}</style></head><body><canvas id="gameCanvas" width="300" height="500"></canvas><script>
const canvas=document.getElementById('gameCanvas'),ctx=canvas.getContext('2d');
let player={x:150,y:400,width:30,height:50};
let obstacles=[],score=0;
let carImg=new Image();carImg.src="assets/car.png";
let roadImg=new Image();roadImg.src="assets/road.png";
canvas.addEventListener('touchmove',(e)=>{let rect=canvas.getBoundingClientRect();player.x=(e.touches[0].clientX-rect.left)*(canvas.width/rect.width);player.x=Math.min(Math.max(player.x,10),canvas.width-40);});
function update(){if(Math.random()<0.02)obstacles.push({x:Math.random()*(canvas.width-30),y:0,w:30,h:30});for(let i=0;i<obstacles.length;i++){obstacles[i].y+=3;if(obstacles[i].y>canvas.height)obstacles.splice(i,1);if(Math.abs(player.x-obstacles[i].x)<30&&Math.abs(player.y-obstacles[i].y)<30){alert('Game Over! Score:'+score);location.reload();}}score++;requestAnimationFrame(frame);}
function draw(){
    ctx.clearRect(0,0,300,500);
    if(roadImg.complete&&roadImg.naturalWidth>0)ctx.drawImage(roadImg,0,0,300,500);
    if(carImg.complete&&carImg.naturalWidth>0)ctx.drawImage(carImg,player.x,player.y,player.width,player.height);
    else{ctx.fillStyle='red';ctx.fillRect(player.x,player.y,player.width,player.height);}
    for(let o of obstacles){ctx.fillStyle='gray';ctx.fillRect(o.x,o.y,o.w,o.h);}
    ctx.fillStyle='white';ctx.fillText('Score:'+score,10,30);
}
function frame(){update();draw();}
frame();
</script></body></html>'''
    },
    "puzzle": {
        "assets": ["tile1","tile2","tile3","background"],
        "html": '''<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1,user-scalable=no"><title>{{TITLE}}</title><style>body{background:#0a0a1a;display:flex;justify-content:center;align-items:center;min-height:100vh;}</style></head><body><canvas id="gameCanvas" width="400" height="500"></canvas><script>
const canvas=document.getElementById('gameCanvas'),ctx=canvas.getContext('2d');
let grid=[],score=0,tileSize=50;
for(let i=0;i<6;i++){grid[i]=[];for(let j=0;j<6;j++)grid[i][j]=Math.floor(Math.random()*3);}
canvas.addEventListener('click',(e)=>{let rect=canvas.getBoundingClientRect();let x=Math.floor((e.clientX-rect.left)*canvas.width/rect.width/tileSize);let y=Math.floor((e.clientY-rect.top)*canvas.height/rect.height/tileSize);if(grid[x]&&grid[y]!==undefined){grid[x][y]=(grid[x][y]+1)%3;score++;}});
function draw(){ctx.clearRect(0,0,400,500);for(let i=0;i<6;i++)for(let j=0;j<6;j++){ctx.fillStyle=`hsl(${grid[i][j]*120},70%,50%)`;ctx.fillRect(i*tileSize,j*tileSize,tileSize-2,tileSize-2);}ctx.fillStyle='white';ctx.fillText('Score:'+score,10,30);requestAnimationFrame(draw);}
draw();
</script></body></html>'''
    },
    "fighting": {
        "assets": ["fighter1","fighter2","background"],
        "html": '''<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1,user-scalable=no"><title>{{TITLE}}</title><style>body{background:#0a0a1a;display:flex;justify-content:center;align-items:center;min-height:100vh;}</style></head><body><canvas id="gameCanvas" width="600" height="300"></canvas><script>
const canvas=document.getElementById('gameCanvas'),ctx=canvas.getContext('2d');
let p1={x:100,y:150,health:100},p2={x:500,y:150,health:100};
canvas.addEventListener('click',()=>{p2.health-=10;if(p2.health<=0)alert('Player 1 wins!');});
function draw(){ctx.clearRect(0,0,600,300);ctx.fillStyle='red';ctx.fillRect(p1.x-25,p1.y-25,50,50);ctx.fillStyle='blue';ctx.fillRect(p2.x-25,p2.y-25,50,50);ctx.fillStyle='white';ctx.fillText('P1 Health:'+p1.health,10,30);ctx.fillText('P2 Health:'+p2.health,500,30);requestAnimationFrame(draw);}
draw();
</script></body></html>'''
    },
    "platformer": {
        "assets": ["player","enemy","platform","background"],
        "html": '''<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1,user-scalable=no"><title>{{TITLE}}</title><style>body{background:#0a0a1a;display:flex;justify-content:center;align-items:center;min-height:100vh;}</style></head><body><canvas id="gameCanvas" width="400" height="500"></canvas><script>
const canvas=document.getElementById('gameCanvas'),ctx=canvas.getContext('2d');
let player={x:50,y:400,width:30,height:30,vy:0,ground:true};
let platforms=[{x:0,y:430,w:400,h:20},{x:150,y:350,w:80,h:20},{x:300,y:280,w:80,h:20}];
let right=false,left=false;
document.addEventListener('keydown',(e)=>{if(e.key==='ArrowRight')right=true;if(e.key==='ArrowLeft')left=true;if(e.key==='ArrowUp'&&player.ground){player.vy=-8;player.ground=false;}});
document.addEventListener('keyup',(e)=>{if(e.key==='ArrowRight')right=false;if(e.key==='ArrowLeft')left=false;});
function update(){
    if(right)player.x+=4;if(left)player.x-=4;
    player.vy+=0.5;player.y+=player.vy;
    player.ground=false;
    for(let p of platforms){if(player.y+player.height>p.y&&player.y<p.y+p.h&&player.x+player.width>p.x&&player.x<p.x+p.w){player.y=p.y-player.height;player.vy=0;player.ground=true;}}
    if(player.y>canvas.height)player.y=0;
    requestAnimationFrame(frame);
}
function draw(){
    ctx.clearRect(0,0,400,500);
    ctx.fillStyle='brown';for(let p of platforms)ctx.fillRect(p.x,p.y,p.w,p.h);
    ctx.fillStyle='red';ctx.fillRect(player.x,player.y,player.width,player.height);
    requestAnimationFrame(frame);
}
function frame(){update();draw();}
frame();
</script></body></html>'''
    }
}

GENRE_TO_TEMPLATE = {
    "local-warfare": "shooter", "offline-fps": "shooter", "shooter": "shooter",
    "soccer": "soccer", "penalty": "soccer",
    "racing": "racing", "drift": "racing",
    "puzzle": "puzzle", "match": "puzzle",
    "fighting": "fighting", "arcade": "fighting",
    "platform": "platformer", "runner": "platformer"
}

def ensure_template_folder(template_name):
    template_dir = os.path.join(config.TEMPLATES_DIR, template_name)
    os.makedirs(template_dir, exist_ok=True)
    assets_json = os.path.join(template_dir, "assets.json")
    if not os.path.exists(assets_json):
        assets_data = {"assets": TEMPLATES[template_name]["assets"]}
        with open(assets_json, "w") as f:
            json.dump(assets_data, f, indent=2)
        send_to_admin(f"📁 Created {assets_json}")
    html_file = os.path.join(template_dir, "game.html")
    if not os.path.exists(html_file):
        with open(html_file, "w") as f:
            f.write(TEMPLATES[template_name]["html"])
        send_to_admin(f"📁 Created {html_file}")
    return True

def get_template_folder(genre):
    genre_lower = genre.lower()
    for key, folder in GENRE_TO_TEMPLATE.items():
        if key in genre_lower:
            return folder
    return "shooter"

def main():
    game, _ = get_current_game()
    if not game:
        send_to_admin("No active game for Phase 3.")
        return
    genre = game["genre"]
    template_name = get_template_folder(genre)
    send_to_admin(f"🛠️ Phase 3 started: building '{genre}' using template '{template_name}'")
    ensure_template_folder(template_name)
    
    # Load plan to get game title
    plan = load_json(os.path.join(config.DATA_DIR, "game_plan.json"))
    game_title = plan.get("game_title", genre.replace("-", " ").title())
    send_to_admin(f"📝 Game title: {game_title}")
    
    src_template = os.path.join(config.TEMPLATES_DIR, template_name, "game.html")
    dst_dir = os.path.join(config.OUTPUT_DIR, "greybox")
    os.makedirs(dst_dir, exist_ok=True)
    dst_file = os.path.join(dst_dir, "game.html")
    
    # Copy and replace title placeholder
    with open(src_template, "r") as f:
        html = f.read()
    html = html.replace("{{TITLE}}", game_title)
    # Also replace <title> fallback if needed
    html = html.replace("<title>Deathroll Studio</title>", f"<title>{game_title}</title>")
    with open(dst_file, "w") as f:
        f.write(html)
    
    # Copy assets.json for phase4
    assets_json_src = os.path.join(config.TEMPLATES_DIR, template_name, "assets.json")
    if os.path.exists(assets_json_src):
        shutil.copy(assets_json_src, os.path.join(config.DATA_DIR, "current_assets.json"))
    
    update_game_status(genre, "phase3_done")
    set_phase_state(4, {"greybox_path": dst_file, "template": template_name, "game_title": game_title})
    send_to_admin(f"✅ Phase 3 complete. Moving to Phase 4 (art).")

if __name__ == "__main__":
    main()
