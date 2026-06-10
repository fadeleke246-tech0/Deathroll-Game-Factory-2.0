const PORTFOLIO_URL = 'https://raw.githubusercontent.com/fadeleke246-tech0/Deathroll-Game-Factory-2.0/main/data/portfolio.json';
const BASE_URL = window.location.origin + window.location.pathname.replace(/\/[^/]*$/, '/');

async function loadGames() {
    const grid = document.getElementById('game-grid');
    grid.innerHTML = '<div class="loading-spinner">🕹️ Fetching latest games...</div>';
    try {
        const res = await fetch(PORTFOLIO_URL + '?t=' + Date.now());
        const data = await res.json();
        const games = data.games || [];
        if (games.length === 0) {
            grid.innerHTML = '<div class="loading-spinner">✨ No games yet. First one incoming soon!</div>';
            return;
        }
        grid.innerHTML = '';
        // Show newest first
        games.reverse().forEach(game => {
            const card = document.createElement('div');
            card.className = 'game-card';
            card.innerHTML = `
                <img src="${game.promo || 'https://placehold.co/512x256/1e2a3a/white?text=Deathroll'}" alt="${game.genre}">
                <h3>${game.genre.toUpperCase().replace(/-/g, ' ')}</h3>
                <p>Playable PWA – installable, offline ready</p>
                <a href="${game.url}" class="play-btn" target="_blank">🎮 PLAY NOW</a>
            `;
            grid.appendChild(card);
        });
    } catch (err) {
        grid.innerHTML = '<div class="loading-spinner">⚠️ Could not load games. Check back later.</div>';
        console.error(err);
    }
}

// Animated stars
function initStars() {
    const canvas = document.getElementById('starsCanvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    let stars = [];
    function resize() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        stars = Array(150).fill().map(() => ({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            r: Math.random() * 2,
            alpha: Math.random() * 0.8
        }));
    }
    function draw() {
        if (!ctx) return;
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = 'white';
        for (let s of stars) {
            ctx.globalAlpha = s.alpha;
            ctx.beginPath();
            ctx.arc(s.x, s.y, s.r, 0, Math.PI * 2);
            ctx.fill();
        }
        requestAnimationFrame(draw);
    }
    window.addEventListener('resize', resize);
    resize();
    draw();
}

loadGames();
initStars();
