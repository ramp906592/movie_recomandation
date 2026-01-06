const API_BASE = "https://movie-recomandation-aga5.onrender.com";
const TMDB_IMG = "https://image.tmdb.org/t/p/w500";

// DOM Elements
const gridContainer = document.getElementById('movie-grid');
const searchInput = document.getElementById('search-input');
const categoryBtns = document.querySelectorAll('.tab-btn');

// --- UTILS ---
// --- FAVORITES SYSTEM (LocalStorage) ---
function getFavorites() {
    return JSON.parse(localStorage.getItem('myMovieList')) || [];
}

function isFavorite(id) {
    const favs = getFavorites();
    return favs.some(m => (m.tmdb_id || m.id) == id);
}

function toggleFavorite(movie, btnElement) {
    let favs = getFavorites();
    let id = movie.tmdb_id || movie.id;
    const idx = favs.findIndex(m => (m.tmdb_id || m.id) == id);

    if (idx > -1) {
        // Remove
        favs.splice(idx, 1);
        btnElement.classList.remove('liked');
        btnElement.innerHTML = '🤍';
    } else {
        // Add
        favs.push(movie);
        btnElement.classList.add('liked');
        btnElement.innerHTML = '❤️';
    }
    localStorage.setItem('myMovieList', JSON.stringify(favs));

    // Show Toast
    const msg = idx > -1 ? "Removed from My List" : "Added to My List";
    showToast(msg);

    // If currently viewing "My List", refresh grid
    if (document.body.dataset.view === 'mylist') {
        renderGrid(favs);
    }
}

function showToast(message) {
    // Remove existing
    const existing = document.querySelector('.toast');
    if (existing) existing.remove();

    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.innerHTML = `<span>${message}</span>`;
    document.body.appendChild(toast);

    // Trigger animation
    setTimeout(() => toast.classList.add('show'), 10);

    // Remove after 3s
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 400);
    }, 3000);
}

function createCard(movie) {
    // Handling different API shapes
    // shape 1: {tmdb_id, title, poster_url, ...}
    // shape 2: {id, title, poster_path, ...} (Raw TMDB)

    let id = movie.tmdb_id || movie.id;
    let title = movie.title || movie.name || "Untitled";
    let poster = movie.poster_url;

    if (!poster && movie.poster_path) {
        poster = TMDB_IMG + movie.poster_path;
    }
    if (!poster) {
        poster = "https://via.placeholder.com/500x750?text=No+Poster";
    }

    let year = (movie.release_date || "").substring(0, 4);
    let rating = movie.vote_average ? `★ ${Number(movie.vote_average).toFixed(1)}` : "";

    const card = document.createElement('div');
    card.className = 'card';

    // Check if favorite
    const liked = isFavorite(id);
    const heartIcon = liked ? '❤️' : '🤍';
    const likedClass = liked ? 'liked' : '';

    // Click on Card -> Go to Details
    card.addEventListener('click', (e) => {
        // Prevent nav if clicked on like button
        if (e.target.classList.contains('like-btn')) return;
        window.location.href = `details.html?id=${id}`;
    });

    card.innerHTML = `
        <img src="${poster}" alt="${title}" loading="lazy">
        <button class="like-btn ${likedClass}">${heartIcon}</button>
        <div class="overlay">
            <h3>${title}</h3>
            <div class="meta">
                <span>${year}</span>
                <span>${rating}</span>
            </div>
        </div>
    `;

    // Attach Like Event
    const likeBtn = card.querySelector('.like-btn');
    likeBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        toggleFavorite(movie, likeBtn);
        // Add small animation feedback
        likeBtn.style.transform = 'scale(1.4)';
        setTimeout(() => likeBtn.style.transform = 'scale(1)', 200);
    });

    return card;
}

function renderGrid(movies) {
    gridContainer.innerHTML = '';
    if (!movies || movies.length === 0) {
        gridContainer.innerHTML = '<p style="color:#aaa; text-align:center; grid-column: 1/-1;">No movies found.</p>';
        return;
    }
    movies.forEach(m => {
        gridContainer.appendChild(createCard(m));
    });
}

async function fetchData(endpoint, params = {}) {
    try {
        const url = new URL(`${API_BASE}${endpoint}`);
        Object.keys(params).forEach(key => url.searchParams.append(key, params[key]));

        const res = await fetch(url);
        if (!res.ok) throw new Error("API Error");
        return await res.json();
    } catch (err) {
        console.error(err);
        return null;
    }
}

// --- HOME PAGE LOGIC ---
async function loadHome(category = "popular") {
    if (!gridContainer) return; // Guard for details page

    gridContainer.innerHTML = '<p style="color:#aaa; text-align:center; grid-column: 1/-1;">Loading...</p>';

    // endpoint mapping
    // API: /home?category=...
    const data = await fetchData('/home', { category: category, limit: 24 });
    renderGrid(data);
}

async function handleSearch(query) {
    if (!query) return;
    gridContainer.innerHTML = '<p style="color:#aaa; text-align:center; grid-column: 1/-1;">Searching...</p>';

    // API: /tmdb/search?query=...
    const data = await fetchData('/tmdb/search', { query: query });
    // This API returns raw TMDB shape: { results: [...] }
    if (data && data.results) {
        renderGrid(data.results);
    } else {
        renderGrid([]);
    }
}

// --- DETAILS PAGE LOGIC ---
async function loadDetails() {
    const params = new URLSearchParams(window.location.search);
    const id = params.get('id');

    if (!id) {
        document.querySelector('.container').innerHTML = "<h1>No Movie ID Provided</h1>";
        return;
    }

    // Load Details
    const data = await fetchData(`/movie/id/${id}`);
    if (!data) {
        document.querySelector('.container').innerHTML = "<h1>Error loading details</h1>";
        return;
    }

    // Populate Info
    document.title = `${data.title} - Details`;
    document.getElementById('poster-img').src = data.poster_url || "https://via.placeholder.com/500x750?text=No+Poster";
    document.getElementById('movie-title').textContent = data.title;
    document.getElementById('movie-overview').textContent = data.overview;
    document.getElementById('movie-release').textContent = `Released: ${data.release_date || 'N/A'}`;

    // Trailer Button Logic
    const trailerBtn = document.querySelector('.details-info button');
    trailerBtn.onclick = () => {
        const query = `${data.title} ${data.release_date ? data.release_date.substring(0, 4) : ''} trailer`;
        window.open(`https://www.youtube.com/results?search_query=${encodeURIComponent(query)}`, '_blank');
    };

    // Genres
    const chipsContainer = document.getElementById('genre-chips');
    if (data.genres) {
        data.genres.forEach(g => {
            const span = document.createElement('span');
            span.className = 'chip';
            span.textContent = g.name;
            chipsContainer.appendChild(span);
        });
    }

    // Load Recommendations (Bundle)
    // We reuse the search logic or recommendation endpoint
    // Let's use /recommend/genre?tmdb_id=... as a fallback or /movie/search if we want powerful ones

    const recContainer = document.getElementById('rec-grid');
    if (recContainer) {
        recContainer.innerHTML = '<p>Loading recommendations...</p>';
        const recs = await fetchData('/recommend/genre', { tmdb_id: id, limit: 12 });
        recContainer.innerHTML = '';
        if (recs && recs.length > 0) {
            recs.forEach(m => recContainer.appendChild(createCard(m)));
        } else {
            recContainer.innerHTML = '<p>No recommendations available.</p>';
        }
    }
}

// --- INIT ---
document.addEventListener('DOMContentLoaded', () => {
    // Check page
    if (document.getElementById('home-page-identifier')) {
        // Home Page
        loadHome('popular');

        // My List Link Listener
        const myListLinks = document.querySelectorAll('nav a[href="#mylist"]');
        myListLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                // Reset active class on nav
                document.querySelectorAll('nav a').forEach(a => a.classList.remove('active'));
                link.classList.add('active');

                document.body.dataset.view = 'mylist';
                document.querySelector('.section-title').textContent = "My Personal List";
                // Hide Tabs
                const tabs = document.querySelector('.category-tabs');
                if (tabs) tabs.style.display = 'none';

                const favs = getFavorites();
                renderGrid(favs);

                // Close sidebar if open
                if (document.getElementById('sidebar').classList.contains('active')) {
                    document.getElementById('menu-btn').click();
                }
            });
        });

        // Search Listener
        let debounceTimer;
        searchInput.addEventListener('input', (e) => {
            clearTimeout(debounceTimer);
            const val = e.target.value.trim();
            debounceTimer = setTimeout(() => {
                if (val.length > 2) {
                    document.querySelector('.section-title').textContent = `Results for "${val}"`;
                    handleSearch(val);
                } else if (val.length === 0) {
                    document.querySelector('.section-title').textContent = "Trending Now";
                    loadHome('popular');
                }
            }, 500);
        });

        // Sidebar Logic
        const menuBtn = document.getElementById('menu-btn');
        const closeBtn = document.getElementById('close-btn');
        const sidebar = document.getElementById('sidebar');
        const overlay = document.getElementById('sidebar-overlay');

        function toggleSidebar() {
            sidebar.classList.toggle('active');
            overlay.classList.toggle('active');
        }

        menuBtn.addEventListener('click', toggleSidebar);
        closeBtn.addEventListener('click', toggleSidebar);
        overlay.addEventListener('click', toggleSidebar);

        // Category Menu Listener (Updated Selector)
        const menuItems = document.querySelectorAll('.menu-item'); // Changed from .tab-btn

        menuItems.forEach(btn => {
            btn.addEventListener('click', () => {
                // remove active class
                menuItems.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');

                const cat = btn.dataset.category;
                document.querySelector('.section-title').textContent = btn.textContent;
                searchInput.value = ''; // clear search
                loadHome(cat);

                // Close sidebar on selection (Mobile feel)
                toggleSidebar();
            });
        });

        // Grid Slider Listener
        const gridSlider = document.getElementById('grid-slider');
        if (gridSlider) {
            gridSlider.addEventListener('input', (e) => {
                const size = e.target.value;
                // Update specific CSS style for grid
                gridContainer.style.gridTemplateColumns = `repeat(auto-fill, minmax(${size}px, 1fr))`;
            });
        }

    } else if (document.getElementById('details-page-identifier')) {
        // Details Page
        loadDetails();
    }
});
