const REPO_BASE = 'https://raw.githubusercontent.com/fadeleke246-tech0/Deathroll-Game-Factory-2.0/main/data/';
const files = {
    queue: 'games_queue.json',
    phase: 'run_state.json',
    portfolio: 'portfolio.json',
    sar: 'sar_analysis.json'
};

async function fetchJSON(file) {
    const res = await fetch(REPO_BASE + file + '?t=' + Date.now());
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return res.json();
}

function formatJSON(data) {
    return JSON.stringify(data, null, 2);
}

function showTab(tabId) {
    document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));
    document.getElementById(tabId).classList.add('active');
    document.querySelectorAll('.sidebar-nav button').forEach(btn => btn.classList.remove('active'));
    document.querySelector(`button[data-tab="${tabId}"]`).classList.add('active');
}

async function loadQueue() {
    const el = document.getElementById('queue-data');
    try {
        const data = await fetchJSON(files.queue);
        el.textContent = formatJSON(data);
    } catch(e) { el.textContent = 'Error: ' + e.message; }
}

async function loadPhase() {
    const el = document.getElementById('phase-data');
    try {
        const data = await fetchJSON(files.phase);
        el.textContent = formatJSON(data);
    } catch(e) { el.textContent = 'Error: ' + e.message; }
}

async function loadPortfolio() {
    const container = document.getElementById('portfolio-grid');
    try {
        const data = await fetchJSON(files.portfolio);
        const games = data.games || [];
        if (games.length === 0) {
            container.innerHTML = '<p>No games shipped yet.</p>';
            return;
        }
        container.innerHTML = '';
        games.slice().reverse().forEach(game => {
            const card = document.createElement('div');
            card.className = 'game-card';
            card.innerHTML = `
                <img src="${game.promo || 'https://placehold.co/512x256'}" style="height:120px">
                <h3 style="font-size:1rem;">${game.genre}</h3>
                <a href="${game.url}" target="_blank" class="play-btn" style="padding:0.3rem;">Play</a>
            `;
            container.appendChild(card);
        });
    } catch(e) { container.innerHTML = '<p>Error loading portfolio</p>'; }
}

async function loadSAR() {
    const el = document.getElementById('sar-data');
    try {
        const data = await fetchJSON(files.sar);
        el.textContent = formatJSON(data);
    } catch(e) { el.textContent = 'No SAR analysis yet.'; }
}

// Event listeners
document.querySelectorAll('.sidebar-nav button').forEach(btn => {
    btn.addEventListener('click', () => {
        const tab = btn.getAttribute('data-tab');
        showTab(tab);
        if (tab === 'queue') loadQueue();
        if (tab === 'phase') loadPhase();
        if (tab === 'portfolio') loadPortfolio();
        if (tab === 'sar') loadSAR();
    });
});

// Load default
showTab('queue');
loadQueue();
