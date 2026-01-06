import requests
import streamlit as st

# =============================
# CONFIG
# =============================
API_BASE = "https://movie-recomandation-aga5.onrender.com/" or "http://127.0.0.1:8000"
TMDB_IMG = "https://image.tmdb.org/t/p/w500"

st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")

# =============================
# STYLES (minimal modern)
# =============================
# =============================
# STYLES (Premium Modern)
# =============================
# =============================
# STYLES (OTT/Netflix-Inspired Premium)
# =============================
# =============================
# STYLES (OTT/Netflix-Inspired Premium)
# =============================
st.markdown(
    """
    <style>
    /* ---------------------------------------------------------------------
       GOOGLE FONTS & BASE
    --------------------------------------------------------------------- */
    @import url('https://fonts.googleapis.com/css2?family=Netflix+Sans:wght@700&family=Inter:wght@300;400;600;800&display=swap');

    :root {
        --primary: #E50914;  /* Netflix Red equivalent or Neon Accent */
        --accent: #6366f1;   /* Neon Indigo */
        --bg-dark: #141414;
        --bg-card: #1f1f1f;
        --text-white: #e5e5e5;
        --text-gray: #b3b3b3;
    }

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        color: var(--text-white);
        background-color: var(--bg-dark);
    }

    /* ---------------------------------------------------------------------
       GLOBAL LAYOUT & BACKGROUND
    --------------------------------------------------------------------- */
    .stApp {
        background-color: var(--bg-dark);
        background-image:
            radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.15) 0px, transparent 50%),
            radial-gradient(at 100% 0%, rgba(229, 9, 20, 0.1) 0px, transparent 50%);
        background-size: 100% 100%;
        background-attachment: fixed;
    }
    
    .block-container {
        padding-top: 2rem;
        padding-bottom: 5rem;
        max-width: 1600px;
    }
    
    /* ---------------------------------------------------------------------
       TYPOGRAPHY AND HEADERS
    --------------------------------------------------------------------- */
    h1, h2, h3 {
        color: white;
        font-weight: 800;
        letter-spacing: -0.5px;
    }
    h1 {
        font-size: 3rem !important;
        background: -webkit-linear-gradient(0deg, #fff, #999);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Decoration/Dividers */
    hr {
        border-color: #333;
        margin: 3em 0;
    }

    /* ---------------------------------------------------------------------
       CUSTOM MOVIE CARD (Netflix Style)
    --------------------------------------------------------------------- */
    .movie-card {
        cursor: pointer;
        position: relative;
        border-radius: 8px;
        overflow: hidden;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        margin-bottom: 1rem;
        aspect-ratio: 2/3;
        background-color: #222;
    }
    
    .movie-card:hover {
        transform: scale(1.05);
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        z-index: 10;
    }

    .movie-card img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        display: block;
        transition: opacity 0.3s;
    }

    /* Overlay on Hover */
    .movie-card .overlay {
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        background: linear-gradient(to top, rgba(0,0,0,0.95), transparent);
        padding: 1rem;
        opacity: 0;
        transform: translateY(20px);
        transition: all 0.3s ease;
        display: flex;
        flex-direction: column;
        justify-content: flex-end;
        height: 100%;
    }
    
    .movie-card:hover .overlay {
        opacity: 1;
        transform: translateY(0);
    }
    
    .movie-card .title {
        color: white;
        font-weight: 700;
        font-size: 1rem;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.8);
        line-height: 1.2;
    }
    
    .movie-card .meta {
        font-size: 0.75rem;
        color: #d1d5db;
        display: flex;
        gap: 8px;
        align-items: center;
    }

    /* ---------------------------------------------------------------------
       SIDEBAR
    --------------------------------------------------------------------- */
    section[data-testid="stSidebar"] {
        background-color: #000000;
        border-right: 1px solid #222;
    }
    section[data-testid="stSidebar"] h2 {
        font-size: 1.2rem;
        color: #e5e5e5;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* ---------------------------------------------------------------------
       INPUTS & BUTTONS (Refined for cleanliness)
    --------------------------------------------------------------------- */
    /* Remove default Streamlit red borders/focus */
    .stTextInput > div[data-baseweb="input"] {
        background-color: #1f1f1f;
        border: 1px solid rgba(255,255,255,0.2) !important;
        border-radius: 50px;
        color: white;
        transition: 0.2s;
    }
    
    /* Focus State */
    .stTextInput > div[data-baseweb="input"]:focus-within {
        background-color: #2a2a2a;
        border-color: var(--accent) !important;
        box-shadow: 0 0 10px rgba(99, 102, 241, 0.5);
    }

    /* Input Text Color */
    .stTextInput input {
        color: white;
    }

    /* Hide the default helper/label if we want cleaner look */
    .stTextInput label {
        display: none !important;
    }

    /* Buttons (Hidden but clickable or minimal) */
    .stButton > button {
        background-color: rgba(255,255,255,0.08);
        color: white;
        border: none;
        border-radius: 4px;
        font-weight: 600;
        transition: 0.2s;
    }
    .stButton > button:hover {
        background-color: white;
        color: black;
        transform: scale(1.02);
    }

    /* ---------------------------------------------------------------------
       DETAILS PAGE
    --------------------------------------------------------------------- */
    .details-hero {
        background: linear-gradient(to right, rgba(20,20,20, 1) 30%, rgba(20,20,20, 0.6) 100%);
        padding: 40px;
        border-radius: 20px;
        margin-bottom: 30px;
        border: 1px solid #333;
        display: flex;
        gap: 30px;
        align-items: flex-start;
    }
    .chip {
        display: inline-block;
        padding: 4px 12px;
        background: rgba(255,255,255,0.1);
        border-radius: 20px;
        font-size: 0.8rem;
        margin-right: 8px;
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    </style>
    """,
    unsafe_allow_html=True,
)

# =============================
# STATE + ROUTING (single-file pages)
# =============================
if "view" not in st.session_state:
    st.session_state.view = "home"  # home | details
if "selected_tmdb_id" not in st.session_state:
    st.session_state.selected_tmdb_id = None

qp_view = st.query_params.get("view")
qp_id = st.query_params.get("id")
if qp_view in ("home", "details"):
    st.session_state.view = qp_view
if qp_id:
    try:
        st.session_state.selected_tmdb_id = int(qp_id)
        st.session_state.view = "details"
    except:
        pass


def goto_home():
    st.session_state.view = "home"
    st.query_params["view"] = "home"
    if "id" in st.query_params:
        del st.query_params["id"]
    st.rerun()


def goto_details(tmdb_id: int):
    st.session_state.view = "details"
    st.session_state.selected_tmdb_id = int(tmdb_id)
    st.query_params["view"] = "details"
    st.query_params["id"] = str(int(tmdb_id))
    st.rerun()


# =============================
# API HELPERS
# =============================
@st.cache_data(ttl=30)  # short cache for autocomplete
def api_get_json(path: str, params: dict | None = None):
    try:
        r = requests.get(f"{API_BASE}{path}", params=params, timeout=25)
        if r.status_code >= 400:
            return None, f"HTTP {r.status_code}: {r.text[:300]}"
        return r.json(), None
    except Exception as e:
        return None, f"Request failed: {e}"


def poster_grid(cards, cols=6, key_prefix="grid"):
    if not cards:
        st.info("No movies to show.")
        return

    rows = (len(cards) + cols - 1) // cols
    idx = 0
    for r in range(rows):
        colset = st.columns(cols, gap="medium")
        for c in range(cols):
            if idx >= len(cards):
                break
            m = cards[idx]
            idx += 1

            tmdb_id = m.get("tmdb_id")
            title = m.get("title", "Untitled")
            poster = m.get("poster_url") or "https://via.placeholder.com/500x750?text=No+Poster"
            
            # Year extraction for meta
            release_date = m.get("release_date", "")
            year = release_date[:4] if release_date else ""

            with colset[c]:
                # Pure HTML Card
                st.markdown(f"""
                <div class="movie-card">
                    <img src="{poster}" loading="lazy" />
                    <div class="overlay">
                        <div class="title">{title}</div>
                        <div class="meta">
                           <span>{year}</span>
                           <span>★ {m.get('vote_average', 0) or ''}</span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Hidden/Minimal Button for interaction (Users click "Open")
                # We label it "View Details" to be clear
                if st.button("▶ Details", key=f"{key_prefix}_{r}_{c}_{idx}_{tmdb_id}"):
                    if tmdb_id:
                        goto_details(tmdb_id)


def to_cards_from_tfidf_items(tfidf_items):
    cards = []
    for x in tfidf_items or []:
        tmdb = x.get("tmdb") or {}
        if tmdb.get("tmdb_id"):
            cards.append(
                {
                    "tmdb_id": tmdb["tmdb_id"],
                    "title": tmdb.get("title") or x.get("title") or "Untitled",
                    "poster_url": tmdb.get("poster_url"),
                }
            )
    return cards


# =============================
# IMPORTANT: Robust TMDB search parsing
# Supports BOTH API shapes:
# 1) raw TMDB: {"results":[{id,title,poster_path,...}]}
# 2) list cards: [{tmdb_id,title,poster_url,...}]
# =============================
def parse_tmdb_search_to_cards(data, keyword: str, limit: int = 24):
    """
    Returns:
      suggestions: list[(label, tmdb_id)]
      cards: list[{tmdb_id,title,poster_url}]
    """
    keyword_l = keyword.strip().lower()

    # A) If API returns dict with 'results'
    if isinstance(data, dict) and "results" in data:
        raw = data.get("results") or []
        raw_items = []
        for m in raw:
            title = (m.get("title") or "").strip()
            tmdb_id = m.get("id")
            poster_path = m.get("poster_path")
            if not title or not tmdb_id:
                continue
            raw_items.append(
                {
                    "tmdb_id": int(tmdb_id),
                    "title": title,
                    "poster_url": f"{TMDB_IMG}{poster_path}" if poster_path else None,
                    "release_date": m.get("release_date", ""),
                }
            )

    # B) If API returns already as list
    elif isinstance(data, list):
        raw_items = []
        for m in data:
            # might be {tmdb_id,title,poster_url}
            tmdb_id = m.get("tmdb_id") or m.get("id")
            title = (m.get("title") or "").strip()
            poster_url = m.get("poster_url")
            if not title or not tmdb_id:
                continue
            raw_items.append(
                {
                    "tmdb_id": int(tmdb_id),
                    "title": title,
                    "poster_url": poster_url,
                    "release_date": m.get("release_date", ""),
                }
            )
    else:
        return [], []

    # Word-match filtering (contains)
    matched = [x for x in raw_items if keyword_l in x["title"].lower()]

    # If nothing matched, fallback to raw list (so never blank)
    final_list = matched if matched else raw_items

    # Suggestions = top 10 labels
    suggestions = []
    for x in final_list[:10]:
        year = (x.get("release_date") or "")[:4]
        label = f"{x['title']} ({year})" if year else x["title"]
        suggestions.append((label, x["tmdb_id"]))

    # Cards = top N
    cards = [
        {"tmdb_id": x["tmdb_id"], "title": x["title"], "poster_url": x["poster_url"]}
        for x in final_list[:limit]
    ]
    return suggestions, cards


# =============================
# SIDEBAR (Compact OTT Style)
# =============================
with st.sidebar:
    st.markdown("## 🍿 MOVIE **HUB**")
    
    # Navigation
    if st.button("🏠 Home", use_container_width=True):
        goto_home()
        
    st.markdown("### 🧭 Discover")
    home_category = st.radio(
        "Browse By:",
        ["trending", "popular", "top_rated", "now_playing", "upcoming"],
        format_func=lambda x: x.replace("_", " ").title(),
        index=0,
    )
    
    st.markdown("---")
    st.caption("🎬 Recommended Settings")
    grid_cols = st.slider("Poster Size (Columns)", 3, 8, 5)


# =============================
# HERO SECTION & SEARCH
# =============================
# We assume 'view=home' usually
if st.session_state.view == "home":
    # Big Hero Header
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center;'>Find your next favorite.</h1>", unsafe_allow_html=True)
    
    # Centered Search Bar
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        typed = st.text_input(
            "Search", 
            placeholder="Search for movies, genres, or actors...", 
            label_visibility="collapsed"
        )
    
    st.markdown("<br>", unsafe_allow_html=True)

    # SEARCH MODE
    if typed.strip():
        if len(typed.strip()) < 2:
            st.warning("Please type at least 2 characters.")
        else:
            with st.spinner("Searching library..."):
                data, err = api_get_json("/tmdb/search", params={"query": typed.strip()})

            if err or data is None:
                st.error(f"Search failed: {err}")
            else:
                # Results Logic
                suggestions, cards = parse_tmdb_search_to_cards(data, typed.strip(), limit=24)
                
                st.markdown(f"### 🔍 Results for '{typed}'")
                poster_grid(cards, cols=grid_cols, key_prefix="search_results")
        
        st.stop() # Stop here if searching

    # HOME FEED
    st.markdown(f"### 🔥 {home_category.replace('_',' ').title()}")
    
    with st.spinner(f"Loading {home_category} movies..."):
        home_cards, err = api_get_json(
            "/home", params={"category": home_category, "limit": 24}
        )
    
    if err or not home_cards:
        st.error(f"Home feed failed: {err or 'Unknown error'}")
        st.stop()

    poster_grid(home_cards, cols=grid_cols, key_prefix="home_feed")


# ==========================================================
# VIEW: DETAILS
# ==========================================================
elif st.session_state.view == "details":
    tmdb_id = st.session_state.selected_tmdb_id
    if not tmdb_id:
        st.warning("No movie selected.")
        if st.button("← Browse"):
            goto_home()
        st.stop()

    # Navigation Bar
    if st.button("← Back to Browse", key="back_btn"):
        goto_home()

    # Fetch Data
    with st.spinner("Fetching details..."):
        data, err = api_get_json(f"/movie/id/{tmdb_id}")
    
    if err or not data:
        st.error(f"Could not load details: {err or 'Unknown error'}")
        st.stop()

    # HERO SECTION (Poster + Info)
    title = data.get("title", "")
    overview = data.get("overview", "")
    poster = data.get("poster_url")
    release = data.get("release_date")
    genres = data.get("genres", [])
    
    # HTML Layout for Hero
    # We use a 2-column layout inside a st.markdown for maximum control, 
    # OR standard columns. Standard columns are safer for images.
    
    st.markdown(f"## {title}")

    col1, col2 = st.columns([1, 2.5], gap="large")
    
    with col1:
        if poster:
            st.image(poster, use_column_width=True)
        else:
            st.markdown("<div style='height:400px; background:#333;'></div>", unsafe_allow_html=True)
            
    with col2:
        # Metadata Chips
        if genres:
            chips_html = "".join([f"<span class='chip'>{g['name']}</span>" for g in genres])
            st.markdown(f"<div style='margin-bottom:1rem;'>{chips_html}</div>", unsafe_allow_html=True)
        
        st.markdown(f"**Released:** {release}")
        st.markdown("### Overview")
        st.write(overview)
        
        st.markdown("<br>", unsafe_allow_html=True)
        # We could add an "Add to Watchlist" button mock here if we had that feature.
        st.button("❤️ Add to Favorites", key="fav_mock")

    st.divider()
    
    # RECOMMENDATIONS
    st.markdown("### 🎬 You might also like")
    
    if title:
        with st.spinner("Finding recommendations..."):
            bundle, err2 = api_get_json(
                "/movie/search",
                params={"query": title, "tfidf_top_n": 10, "genre_limit": 10},
            )

        if not err2 and bundle:
            # Combined or Tabs
            t1, t2 = st.tabs(["Similar Movies", "More in this Genre"])
            
            with t1:
                poster_grid(
                    to_cards_from_tfidf_items(bundle.get("tfidf_recommendations")),
                    cols=grid_cols,
                    key_prefix="details_tfidf",
                )
            with t2:
                poster_grid(
                    bundle.get("genre_recommendations", []),
                    cols=grid_cols,
                    key_prefix="details_genre",
                )
        else:
            st.info("No automatic recommendations found. Here are some genre picks.")
            genre_only, err3 = api_get_json(
                "/recommend/genre", params={"tmdb_id": tmdb_id, "limit": 10}
            )
            poster_grid(genre_only, cols=grid_cols or 4, key_prefix="fallback_genre")
    else:
        st.warning("Data incomplete for recommendations.")