<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Deathroll Factory – Professional Dashboard</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,300;14..32,400;14..32,600;14..32,700&display=swap" rel="stylesheet">
    <style>
        /* ---------- Reset & Base ---------- */
        * { margin:0; padding:0; box-sizing:border-box; }
        body {
            background: radial-gradient(circle at 10% 20%, #0b0b1a, #03030c);
            color: #f0f3fa;
            font-family: 'Inter', sans-serif;
            min-height: 100vh;
            padding: 2rem;
        }
        a { color: #ffb347; text-decoration: none; }
        .container { max-width: 1400px; margin: 0 auto; }

        /* ---------- Glassmorphism Card ---------- */
        .glass {
            background: rgba(20, 25, 45, 0.65);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 2rem;
            padding: 1.5rem 2rem;
            box-shadow: 0 20px 40px -12px rgba(0,0,0,0.5);
            transition: transform 0.25s ease, box-shadow 0.25s ease;
        }
        .glass:hover { transform: translateY(-2px); box-shadow: 0 30px 50px -16px rgba(0,0,0,0.6); }

        /* ---------- Header ---------- */
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            margin-bottom: 2rem;
        }
        .logo h1 {
            background: linear-gradient(135deg, #ffb347, #ff6b6b);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            font-size: 2.2rem;
            font-weight: 700;
        }
        .logo span { font-size: 0.9rem; color: #9aa3bf; display: block; }
        .status-badge {
            background: #1e2a3a;
            padding: 0.4rem 1.2rem;
            border-radius: 40px;
            font-size: 0.85rem;
            border: 1px solid rgba(255,255,255,0.1);
        }
        .status-badge .dot {
            display: inline-block;
            width: 10px;
            height: 10px;
            border-radius: 50%;
            margin-right: 0.5rem;
            background: #4caf50;
        }
        .status-badge .dot.warning { background: #ffb347; }
        .status-badge .dot.error { background: #ff6b6b; }

        /* ---------- Grid Layout ---------- */
        .dashboard-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1.5rem;
            margin-bottom: 2rem;
        }
        @media (max-width: 1000px) { .dashboard-grid { grid-template-columns: 1fr; } }

        /* ---------- Form Elements ---------- */
        .form-group { margin-bottom: 1.2rem; }
        .form-group label {
            display: block;
            font-weight: 600;
            font-size: 0.85rem;
            margin-bottom: 0.3rem;
            color: #cbd5f0;
        }
        .form-group input, .form-group select, .form-group textarea {
            width: 100%;
            padding: 0.7rem 1rem;
            background: rgba(0,0,0,0.3);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 1rem;
            color: white;
            font-family: 'Inter', sans-serif;
            font-size: 0.95rem;
            transition: border-color 0.2s;
        }
        .form-group input:focus, .form-group select:focus, .form-group textarea:focus {
            outline: none;
            border-color: #ffb347;
        }
        .form-group textarea { resize: vertical; min-height: 80px; }

        /* ---------- Buttons ---------- */
        .btn {
            background: linear-gradient(135deg, #ff6b6b, #ffb347);
            border: none;
            padding: 0.8rem 2rem;
            border-radius: 40px;
            font-weight: 600;
            color: white;
            cursor: pointer;
            font-size: 1rem;
            transition: opacity 0.2s, transform 0.1s;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
        }
        .btn:hover { opacity: 0.9; transform: scale(1.01); }
        .btn:active { transform: scale(0.98); }
        .btn-secondary {
            background: rgba(255,255,255,0.08);
            backdrop-filter: blur(4px);
            border: 1px solid rgba(255,255,255,0.1);
        }
        .btn-secondary:hover { background: rgba(255,255,255,0.15); }

        /* ---------- Logs ---------- */
        .log-area {
            background: #0a0e16;
            border-radius: 1.5rem;
            padding: 1rem;
            font-family: 'Monaco', 'Menlo', monospace;
            font-size: 0.75rem;
            max-height: 300px;
            overflow-y: auto;
            white-space: pre-wrap;
            word-wrap: break-word;
            border: 1px solid rgba(255,255,255,0.05);
            color: #b0c0d0;
        }
        .log-area .timestamp { color: #6f7a99; }
        .log-area .info { color: #4fc3f7; }
        .log-area .success { color: #81c784; }
        .log-area .error { color: #ef5350; }

        /* ---------- Game Gallery ---------- */
        .game-gallery {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
            gap: 1rem;
            margin-top: 1rem;
        }
        .game-item {
            background: rgba(0,0,0,0.3);
            border-radius: 1.2rem;
            overflow: hidden;
            transition: transform 0.2s;
            border: 1px solid rgba(255,255,255,0.05);
        }
        .game-item:hover { transform: translateY(-4px); border-color: #ffb347; }
        .game-item img {
            width: 100%;
            height: 120px;
            object-fit: cover;
            background: #1a1f2e;
        }
        .game-item .info { padding: 0.6rem 0.8rem; }
        .game-item .title { font-weight: 600; font-size: 0.9rem; }
        .game-item .genre { font-size: 0.7rem; color: #9aa3bf; }
        .game-item .play-link {
            display: block;
            margin-top: 0.4rem;
            text-align: center;
            background: rgba(255,107,107,0.2);
            padding: 0.3rem;
            border-radius: 30px;
            font-size: 0.7rem;
            font-weight: 600;
            color: #ffb347;
            transition: background 0.2s;
        }
        .game-item .play-link:hover { background: rgba(255,107,107,0.3); }

        /* ---------- Token Input ---------- */
        .token-input {
            display: flex;
            gap: 0.5rem;
            align-items: center;
        }
        .token-input input { flex: 1; }
        .token-input .btn { padding: 0.5rem 1.2rem; font-size: 0.85rem; }

        /* ---------- Status Cards ---------- */
        .stat-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 0.8rem;
            margin-top: 0.8rem;
        }
        .stat-card {
            background: rgba(0,0,0,0.2);
            border-radius: 1rem;
            padding: 0.8rem;
            text-align: center;
        }
        .stat-card .value { font-size: 1.8rem; font-weight: 700; color: #ffb347; }
        .stat-card .label { font-size: 0.7rem; color: #9aa3bf; text-transform: uppercase; letter-spacing: 0.5px; }

        /* ---------- Responsive ---------- */
        @media (max-width: 600px) {
            body { padding: 1rem; }
            .glass { padding: 1rem; }
            .header { flex-direction: column; align-items: flex-start; gap: 0.5rem; }
            .dashboard-grid { grid-template-columns: 1fr; }
            .game-gallery { grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); }
        }

        /* ---------- Scrollbar ---------- */
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: #0a0e16; border-radius: 10px; }
        ::-webkit-scrollbar-thumb { background: #2a2f40; border-radius: 10px; }
        ::-webkit-scrollbar-thumb:hover { background: #4a4f60; }
    </style>
</head>
<body>
<div class="container">

    <!-- Header -->
    <header class="header glass">
        <div class="logo">
            <h1>🏭 Deathroll Factory</h1>
            <span>Autonomous Game Generation Platform</span>
        </div>
        <div class="status-badge" id="statusBadge">
            <span class="dot" id="statusDot"></span>
            <span id="statusText">Connecting...</span>
        </div>
    </header>

    <!-- Main Grid -->
    <div class="dashboard-grid">

        <!-- Left: Control Panel -->
        <div class="glass">
            <h2 style="margin-bottom:1.2rem;">🎮 New Game</h2>
            <form id="buildForm">
                <div class="form-group">
                    <label for="genre">Genre</label>
                    <select id="genre" required>
                        <option value="shooter">Shooter</option>
                        <option value="soccer">Soccer</option>
                        <option value="racing">Racing</option>
                        <option value="platformer">Platformer</option>
                        <option value="puzzle">Puzzle</option>
                        <option value="rpg">RPG</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="graphics">Graphics Quality</label>
                    <select id="graphics" required>
                        <option value="low">Low (Pixel Art)</option>
                        <option value="medium">Medium (2D)</option>
                        <option value="high">High (3D)</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="customPrompt">Custom Prompt (optional)</label>
                    <textarea id="customPrompt" placeholder="e.g. 'Cyberpunk theme with neon lights'"></textarea>
                </div>
                <div class="form-group token-input">
                    <input type="password" id="githubToken" placeholder="GitHub Personal Access Token (required)" />
                    <button type="button" class="btn btn-secondary" id="tokenHelp">?</button>
                </div>
                <button type="submit" class="btn" id="triggerBtn">
                    <span>🚀</span> Generate Game
                </button>
            </form>
            <div id="formStatus" style="margin-top:1rem; font-size:0.9rem;"></div>
        </div>

        <!-- Right: Status & Logs -->
        <div class="glass">
            <h2 style="margin-bottom:1.2rem;">📊 Live Status</h2>
            <div class="stat-grid" id="statGrid">
                <div class="stat-card"><div class="value" id="statPhase">-</div><div class="label">Current Phase</div></div>
                <div class="stat-card"><div class="value" id="statGames">0</div><div class="label">Games Shipped</div></div>
                <div class="stat-card"><div class="value" id="statQueue">0</div><div class="label">Queue</div></div>
            </div>
            <div style="margin-top:1.2rem;">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.5rem;">
                    <span style="font-weight:600;">📋 Activity Log</span>
                    <button class="btn btn-secondary" style="padding:0.2rem 0.8rem;font-size:0.7rem;" id="clearLog">Clear</button>
                </div>
                <div class="log-area" id="logArea">⏳ Waiting for events...</div>
            </div>
        </div>
    </div>

    <!-- Game Gallery -->
    <div class="glass" style="margin-bottom:2rem;">
        <h2 style="margin-bottom:1rem;">🎲 Game Vault</h2>
        <div id="gameGallery" class="game-gallery">
            <div style="grid-column:1/-1; text-align:center; color:#9aa3bf;">Loading games...</div>
        </div>
    </div>

    <!-- Footer -->
    <footer style="text-align:center;font-size:0.7rem;color:#4a5570;margin-top:2rem;">
        Powered by Deathroll Factory Bot &bull; Data refreshes automatically
    </footer>
</div>

<script>
    // ---------- Configuration ----------
    const REPO_OWNER = 'fadeleke246-tech0';
    const REPO_NAME = 'Deathroll-Game-Factory-2.0';
    const GITHUB_API_BASE = `https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}`;
    const RAW_BASE = `https://raw.githubusercontent.com/${REPO_OWNER}/${REPO_NAME}/main`;

    // ---------- DOM refs ----------
    const logArea = document.getElementById('logArea');
    const formStatus = document.getElementById('formStatus');
    const triggerBtn = document.getElementById('triggerBtn');
    const buildForm = document.getElementById('buildForm');
    const githubTokenInput = document.getElementById('githubToken');
    const statPhase = document.getElementById('statPhase');
    const statGames = document.getElementById('statGames');
    const statQueue = document.getElementById('statQueue');
    const gameGallery = document.getElementById('gameGallery');
    const statusDot = document.getElementById('statusDot');
    const statusText = document.getElementById('statusText');

    // ---------- Logging ----------
    function addLog(message, type = 'info') {
        const timestamp = new Date().toLocaleTimeString();
        const entry = document.createElement('div');
        entry.innerHTML = `<span class="timestamp">[${timestamp}]</span> <span class="${type}">${message}</span>`;
        logArea.appendChild(entry);
        logArea.scrollTop = logArea.scrollHeight;
        // Keep last 100 entries
        while (logArea.children.length > 100) logArea.removeChild(logArea.firstChild);
    }

    document.getElementById('clearLog').addEventListener('click', () => { logArea.innerHTML = ''; });

    // ---------- Fetch helpers ----------
    async function fetchJSON(url) {
        const res = await fetch(url + '?t=' + Date.now());
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
    }

    // ---------- Update Status ----------
    async function updateStatus() {
        try {
            // Phase
            const state = await fetchJSON(`${RAW_BASE}/data/run_state.json`);
            const phase = state.phase || 'N/A';
            statPhase.textContent = phase;
            // Queue
            const queue = await fetchJSON(`${RAW_BASE}/data/games_queue.json`);
            const queueCount = Object.keys(queue).filter(k => queue[k].status !== 'completed').length;
            statQueue.textContent = queueCount;
            // Portfolio
            const portfolio = await fetchJSON(`${RAW_BASE}/data/portfolio.json`);
            const count = Object.keys(portfolio).length;
            statGames.textContent = count;
            // Dot
            statusDot.className = 'dot' + (phase <= 7 ? '' : ' warning');
            statusText.textContent = phase <= 7 ? `Phase ${phase}` : 'Idle';
            return { state, queue, portfolio };
        } catch (e) {
            statusDot.className = 'dot error';
            statusText.textContent = 'Offline';
            addLog('⚠️ Failed to fetch status: ' + e.message, 'error');
        }
    }

    // ---------- Render Gallery ----------
    function renderGallery(portfolio) {
        const games = Object.values(portfolio);
        if (games.length === 0) {
            gameGallery.innerHTML = '<div style="grid-column:1/-1;text-align:center;color:#9aa3bf;">No games shipped yet.</div>';
            return;
        }
        let html = '';
        games.slice().reverse().forEach(g => {
            html += `
                <div class="game-item">
                    <img src="${g.promo || 'https://placehold.co/400x200/1e2a3a/white?text=No+Image'}" alt="${g.title}">
                    <div class="info">
                        <div class="title">${g.title}</div>
                        <div class="genre">${g.genre || ''}</div>
                        <a href="${g.game_url || '#'}" target="_blank" class="play-link">🎮 Play</a>
                    </div>
                </div>
            `;
        });
        gameGallery.innerHTML = html;
    }

    // ---------- Trigger Build ----------
    buildForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const token = githubTokenInput.value.trim();
        if (!token) {
            formStatus.innerHTML = '❌ Please enter your GitHub Personal Access Token.';
            return;
        }
        const genre = document.getElementById('genre').value;
        const graphics = document.getElementById('graphics').value;
        const prompt = document.getElementById('customPrompt').value.trim();

        triggerBtn.disabled = true;
        triggerBtn.innerHTML = '⏳ Sending...';
        formStatus.innerHTML = '';

        try {
            const resp = await fetch(`${GITHUB_API_BASE}/actions/workflows/factory.yml/dispatches`, {
                method: 'POST',
                headers: {
                    'Authorization': `token ${token}`,
                    'Accept': 'application/vnd.github.v3+json'
                },
                body: JSON.stringify({
                    ref: 'main',
                    inputs: { genre, graphics, prompt }
                })
            });
            if (resp.ok) {
                formStatus.innerHTML = '✅ Build triggered successfully! Check logs for progress.';
                addLog('🚀 Triggered new game build: ' + genre + ' (' + graphics + ')', 'success');
                // Poll for status update
                setTimeout(updateStatus, 5000);
            } else {
                const err = await resp.text();
                formStatus.innerHTML = `❌ Failed: ${err}`;
                addLog('❌ Build trigger failed: ' + err, 'error');
            }
        } catch (err) {
            formStatus.innerHTML = `❌ Error: ${err.message}`;
            addLog('❌ Error triggering build: ' + err.message, 'error');
        } finally {
            triggerBtn.disabled = false;
            triggerBtn.innerHTML = '🚀 Generate Game';
        }
    });

    // ---------- Token help ----------
    document.getElementById('tokenHelp').addEventListener('click', () => {
        alert('To generate a token:\n1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)\n2. Generate a new token with "repo" and "workflow" scopes.\n3. Copy and paste it here.');
    });

    // ---------- Initial load & polling ----------
    async function refreshAll() {
        const data = await updateStatus();
        if (data && data.portfolio) renderGallery(data.portfolio);
        addLog('🔄 Dashboard refreshed', 'info');
    }

    // Refresh every 30 seconds
    refreshAll();
    setInterval(refreshAll, 30000);

    // Also update on visibility change (when user returns to tab)
    document.addEventListener('visibilitychange', () => {
        if (!document.hidden) refreshAll();
    });

    // ---------- Quick initial log ----------
    addLog('✅ Dashboard ready. Waiting for data...', 'success');
</script>
</body>
</html>
