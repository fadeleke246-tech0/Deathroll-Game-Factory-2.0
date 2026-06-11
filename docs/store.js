const PORTFOLIO_URL = 'https://raw.githubusercontent.com/fadeleke246-tech0/Deathroll-Game-Factory-2.0/main/data/portfolio.json';
async function loadGames() {
    const grid = document.getElementById('game-grid');
    grid.innerHTML = '<div class="loading-spinner">🕹️ Fetching latest games...</div>';
    try {
        const res = await fetch(PORTFOLIO_URL + '?t=' + Date.now());
        const data = await res.json();
        const games = Object.values(data);
        if (games.length === 0) { grid.innerHTML = '<div class="loading-spinner">✨ No games yet. First one incoming soon!</div>'; return; }
        grid.innerHTML = '';
        games.reverse().forEach(game => {
            const card = document.createElement('div');
            card.className = 'game-card';
            card.innerHTML = `
                <img src="${game.promo || 'https://placehold.co/512x256/1e2a3a/white?text=Deathroll'}" alt="${game.title}">
                <h3>${game.title}</h3>
                <p>${game.concept?.substring(0,100) || ''}</p>
                <a href="${game.game_url}" class="play-btn" target="_blank">🎮 PLAY NOW</a>
            `;
            grid.appendChild(card);
        });
    } catch(err) { grid.innerHTML = '<div class="loading-spinner">⚠️ Could not load games.</div>'; }
}
loadGames();
