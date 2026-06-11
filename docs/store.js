// docs/store.js – Loads games from portfolio.json and displays them
async function loadGames() {
    const response = await fetch('https://raw.githubusercontent.com/YOUR_USERNAME/Deathroll-Game-Factory-2.0/main/data/portfolio.json');
    const games = await response.json();
    const container = document.getElementById('game-grid');
    container.innerHTML = '';

    for (const [id, game] of Object.entries(games)) {
        const card = document.createElement('div');
        card.className = 'game-card';
        card.innerHTML = `
            <img src="${game.promo || 'https://via.placeholder.com/300x200?text=No+Image'}" 
                 alt="${game.title}"
                 onerror="this.src='https://via.placeholder.com/300x200?text=Placeholder'">
            <h3>${game.title}</h3>
            <p>${game.concept.substring(0, 100)}...</p>
            <a href="${game.game_url}" target="_blank">Play Now</a>
        `;
        container.appendChild(card);
    }
}
loadGames();
