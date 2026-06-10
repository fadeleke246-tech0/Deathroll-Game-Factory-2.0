const GAME_DATA_URL = 'https://raw.githubusercontent.com/fadeleke246-tech0/deathroll-factory/main/data/portfolio.json';
const BASE_URL = window.location.origin + window.location.pathname.replace(/\/[^/]*$/, '/');

async function loadGames() {
    const grid = document.getElementById('game-grid');
    grid.innerHTML = '<div class="loading-spinner">Loading game vault...</div>';
    try {
        const res = await fetch(GAME_DATA_URL + '?t=' + Date.now());
        const data = await res.json();
        const games = data.games || [];
        if (games.length === 0) {
            grid.innerHTML = '<div class="loading-spinner">No games yet. First one incoming soon! 🚀</div>';
            return;
        }
        grid.innerHTML = '';
        games.reverse().forEach(game => {
            const card = document.createElement('div');
            card.className = 'game-card';
            card.innerHTML = `
                <img src="${game.promo || 'https://placehold.co/512x256/1e2a3a/white?text=Deathroll'}" alt="${game.genre}">
                <h3>${game.genre.replace(/-/g, ' ').toUpperCase()}</h3>
                <p>Play now — installable PWA</p>
                <a href="${game.url}" class="play-btn" target="_blank">🎮 PLAY</a>
            `;
            grid.appendChild(card);
        });
    } catch (err) {
        grid.innerHTML = '<div class="loading-spinner">⚠️ Could not load games. Check back later.</div>';
        console.error(err);
    }
}
loadGames();
