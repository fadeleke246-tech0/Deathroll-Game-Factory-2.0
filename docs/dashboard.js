const REPO_BASE = 'https://raw.githubusercontent.com/fadeleke246-tech0/deathroll-factory/main/data/';
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

function showTab(tabId) {
    document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));
    document.getElementById(tabId).classList.add('active');
    document.querySelectorAll('.sidebar button').forEach(btn => btn.classList.remove('active'));
    document.querySelector(`button[data-tab="${tabId}"]`).classList.add('active');
}

async function loadQueue() {
    const el = document.getElementById('queue-data');
    try {
        const data = await fetchJSON(files.queue);
        el.textContent = JSON.stringify(data, null, 2);
    } catch(e) { el.textContent = 'Error loading queue: ' + e.message; }
}
async function loadPhase() {
    const el = document.getElementById('phase-data');
    try {
        const data = await fetchJSON(files.phase);
        el.textContent = JSON.stringify(data, null, 2);
    } catch(e) { el.textContent = 'Error loading phase state'; }
}
async function loadPortfolio() {
    const container = document.getElementById('portfolio-grid');
    try {
        const data = await fetchJSON(files.portfolio);
        const games = data.games || [];
        if (!games.length) { container.innerHTML = '<p>No games shipped yet.</p>'; return; }
        container.innerHTML = '';
        games.reverse().forEach(game => {
            const card = document.createElement('div');
            card.className = 'game-card';
            card.innerHTML = `
                <img src="${game.promo || 'https://placehold.co/512x256'}" style="height:120px">
                <h3>${game.genre}</h3>
                <a href="${game.url}" target="_blank" class="play-btn">Play</a>
            `;
            container.appendChild(card);
        });
    } catch(e) { container.innerHTML = '<p>Error loading portfolio</p>'; }
}
async function loadSAR() {
    const el = document.getElementById('sar-data');
    try {
        const data = await fetchJSON(files.sar);
        el.textContent = JSON.stringify(data, null, 2);
    } catch(e) { el.textContent = 'No SAR analysis yet.'; }
}

document.querySelectorAll('.sidebar button').forEach(btn => {
    btn.addEventListener('click', () => {
        const tab = btn.getAttribute('data-tab');
        showTab(tab);
        if (tab === 'queue') loadQueue();
        if (tab === 'phase') loadPhase();
        if (tab === 'portfolio') loadPortfolio();
        if (tab === 'sar') loadSAR();
    });
});
// Load default tab
showTab('queue');
loadQueue();
