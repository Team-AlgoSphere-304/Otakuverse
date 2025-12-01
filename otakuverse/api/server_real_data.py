"""
OtakuVerse - Real Data Edition with Actual MAL/IMDb APIs
Fetches fresh recommendations from real sources instead of pre-loaded catalogs
"""

import os
import sys
import asyncio
import random
from datetime import datetime
from typing import Optional, List

# Load .env
def load_env_file():
    # Try multiple possible locations
    possible_paths = [
        os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), '.env'),  # ../../.env
        os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env'),  # ../.env
        os.path.join(os.getcwd(), '.env'),  # Current working directory
    ]
    
    env_file = None
    for path in possible_paths:
        if os.path.exists(path):
            env_file = path
            print(f"[INFO] Loading .env from: {env_file}")
            break
    
    if not env_file:
        print(f"[WARNING] .env file not found in any location: {possible_paths}")
        return
    
    with open(env_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                if '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip().strip('"').strip("'")
                    value = value.strip().strip('"').strip("'")
                    if key not in os.environ:
                        os.environ[key] = value
                        print(f"[ENV] {key} = {value[:20]}..." if len(value) > 20 else f"[ENV] {key} = {value}")

load_env_file()

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx

# API Keys
OMDB_API_KEY = os.getenv("OMDB_API_KEY", "")
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY", "")
MAL_CLIENT_ID = os.getenv("MAL_CLIENT_ID", "")

# Initialize FastAPI
app = FastAPI(
    title="OtakuVerse - Real Data Edition",
    description="Live recommendations from MAL and IMDb APIs",
    version="3.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class RecommendationRequest(BaseModel):
    user_id: str
    genres: Optional[List[str]] = None
    moods: Optional[List[str]] = None
    content_types: List[str]
    exclude_titles: Optional[List[str]] = None
    count: Optional[int] = 15

# In-memory storage
user_history = {}
user_watchlater = {}
user_settings = {}
search_cache = {}  # Cache search results for persistent catalog


# ==================== MAL API Functions ====================

async def fetch_mal_anime(query: str, limit: int = 10) -> List[dict]:
    """Fetch anime from MyAnimeList API"""
    if not MAL_CLIENT_ID:
        print("[WARNING] MAL_CLIENT_ID not configured")
        return []
    
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            headers = {"X-MAL-CLIENT-ID": MAL_CLIENT_ID}
            
            # Properly encode the query
            params = {
                "query": query.strip(),
                "limit": min(limit, 25),
                "fields": "id,title,mean,main_picture,genres,synopsis,status,num_episodes"
            }
            
            response = await client.get(
                "https://api.myanimelist.net/v2/anime/search",
                params=params,
                headers=headers
            )
            
            if response.status_code == 200:
                data = response.json()
                results = data.get("data", [])
                if results:
                    print(f"[MAL API] ✓ Found {len(results)} results for '{query}'")
                    return results
                else:
                    print(f"[MAL API] ✗ No results for '{query}'")
                    return []
            else:
                print(f"[MAL API] Error {response.status_code}: {response.text}")
                return []
    except Exception as e:
        print(f"[ERROR] MAL API exception: {str(e)}")
        return []


async def fetch_mal_manga(query: str, limit: int = 10) -> List[dict]:
    """Fetch manga from MyAnimeList API"""
    if not MAL_CLIENT_ID:
        print("[WARNING] MAL_CLIENT_ID not configured")
        return []
    
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            headers = {"X-MAL-CLIENT-ID": MAL_CLIENT_ID}
            
            params = {
                "query": query.strip(),
                "limit": min(limit, 25),
                "fields": "id,title,mean,main_picture,genres,synopsis,status"
            }
            
            response = await client.get(
                "https://api.myanimelist.net/v2/manga/search",
                params=params,
                headers=headers
            )
            
            if response.status_code == 200:
                data = response.json()
                results = data.get("data", [])
                if results:
                    print(f"[MAL API] ✓ Found {len(results)} manga results for '{query}'")
                    return results
                else:
                    print(f"[MAL API] ✗ No manga results for '{query}'")
                    return []
            else:
                print(f"[MAL API] Error {response.status_code}: {response.text}")
                return []
    except Exception as e:
        print(f"[ERROR] MAL Manga API exception: {str(e)}")
        return []


# ==================== IMDb Functions ====================

async def fetch_imdb_movies(query: str, year: Optional[int] = None) -> List[dict]:
    """Fetch movies from OMDb (IMDb API)"""
    if not OMDB_API_KEY:
        print("[WARNING] OMDB_API_KEY not set")
        return []
    
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(
                "http://www.omdbapi.com/",
                params={
                    "apikey": OMDB_API_KEY,
                    "s": query,
                    "type": "movie",
                    "page": 1
                }
            )
            if response.status_code == 200:
                data = response.json()
                if data.get("Response") == "True":
                    return data.get("Search", [])
    except Exception as e:
        print(f"[ERROR] IMDb API: {e}")
    return []


async def fetch_imdb_series(query: str) -> List[dict]:
    """Fetch TV series from OMDb"""
    if not OMDB_API_KEY:
        return []
    
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(
                "http://www.omdbapi.com/",
                params={
                    "apikey": OMDB_API_KEY,
                    "s": query,
                    "type": "series",
                    "page": 1
                }
            )
            if response.status_code == 200:
                data = response.json()
                if data.get("Response") == "True":
                    return data.get("Search", [])
    except Exception as e:
        print(f"[ERROR] IMDb Series API: {e}")
    return []


# ==================== Recommendation Logic ====================

async def get_random_query(content_type: str) -> str:
    """Get a smart search query based on content type and mood"""
    queries = {
        "anime": ["action", "romance", "fantasy", "mystery", "thriller", "comedy", "horror", "supernatural", "school", "adventure", "psychological", "slice of life", "isekai", "mecha", "sports"],
        "manga": ["thriller", "mystery", "romance", "fantasy", "action", "psychological", "horror", "adventure", "slice of life", "comedy", "drama", "shounen"],
        "movies": ["thriller", "action", "drama", "sci-fi", "fantasy", "horror", "comedy", "adventure", "mystery", "romance"],
        "web_series": ["thriller", "drama", "sci-fi", "fantasy", "comedy", "horror", "adventure", "mystery", "psychological"],
    }
    
    query_list = queries.get(content_type, ["popular"])
    return random.choice(query_list)


async def get_smart_query(content_type: str, genres: list, moods: list) -> str:
    """Get a smart search query based on user genres and moods"""
    if genres and len(genres) > 0:
        return random.choice(genres)
    
    if moods:
        mood_to_genre = {
            "happy": "comedy",
            "sad": "drama",
            "excited": "action",
            "relaxed": "slice of life",
            "tense": "thriller",
            "romantic": "romance",
            "thoughtful": "psychological",
            "adventurous": "adventure",
        }
        for mood in moods:
            if mood.lower() in mood_to_genre:
                return mood_to_genre[mood.lower()]
    
    return await get_random_query(content_type)


async def format_anime_recommendation(mal_anime: dict, exclude_titles: List[str]) -> Optional[dict]:
    """Convert MAL anime to recommendation format"""
    if not mal_anime:
        return None
    
    anime = mal_anime.get("node", {})
    title = anime.get("title", "")
    
    # Skip if excluded
    if exclude_titles and title.lower() in [t.lower() for t in exclude_titles]:
        return None
    
    return {
        "content_id": f"anime_{anime.get('id')}",
        "title": title,
        "content_type": "anime",
        "genres": [g.get("name") for g in anime.get("genres", [])],
        "rating": anime.get("mean", 0),
        "mal_score": anime.get("mean", 0),
        "description": anime.get("synopsis", ""),
        "cover_image": anime.get("main_picture", {}).get("medium_url", ""),
        "episodes": anime.get("num_episodes", 0),
        "status": anime.get("status", ""),
    }


async def format_manga_recommendation(mal_manga: dict, exclude_titles: List[str]) -> Optional[dict]:
    """Convert MAL manga to recommendation format"""
    if not mal_manga:
        return None
    
    manga = mal_manga.get("node", {})
    title = manga.get("title", "")
    
    if exclude_titles and title.lower() in [t.lower() for t in exclude_titles]:
        return None
    
    return {
        "content_id": f"manga_{manga.get('id')}",
        "title": title,
        "content_type": "manga",
        "genres": [g.get("name") for g in manga.get("genres", [])],
        "rating": manga.get("mean", 0),
        "mal_score": manga.get("mean", 0),
        "description": manga.get("synopsis", ""),
        "cover_image": manga.get("main_picture", {}).get("medium_url", ""),
        "status": manga.get("status", ""),
    }


async def format_imdb_recommendation(imdb_data: dict, content_type: str, exclude_titles: List[str]) -> Optional[dict]:
    """Convert IMDb data to recommendation format"""
    if not imdb_data:
        return None
    
    title = imdb_data.get("Title", "")
    
    if exclude_titles and title.lower() in [t.lower() for t in exclude_titles]:
        return None
    
    try:
        rating = float(imdb_data.get("imdbRating", "0"))
    except:
        rating = 0
    
    return {
        "content_id": imdb_data.get("imdbID", ""),
        "title": title,
        "content_type": content_type,
        "genres": imdb_data.get("Type", "").split(","),
        "rating": rating,
        "imdb_score": rating,
        "description": imdb_data.get("Plot", ""),
        "cover_image": imdb_data.get("Poster", ""),
        "year": imdb_data.get("Year", ""),
    }


# ==================== Endpoints ====================

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }


@app.post("/recommendations")
async def get_recommendations(request: RecommendationRequest):
    """
    Get SMART recommendations based on genres and moods.
    - Uses genres/moods to search for relevant content
    - Filters by rating for quality
    - No pre-loaded catalogs - all fresh from APIs
    """
    try:
        if not request.content_types:
            raise HTTPException(status_code=400, detail="content_types required")
        
        recommendations = []
        exclude_titles = [t.lower() for t in (request.exclude_titles or [])]
        target_count = min(request.count or 15, 50)
        
        # Fetch from APIs based on content types using SMART queries
        tasks = []
        content_queries = []
        
        for content_type in request.content_types:
            # Get smart query based on user's genres and moods
            smart_query = await get_smart_query(content_type, request.genres or [], request.moods or [])
            content_queries.append((content_type, smart_query))
            
            if content_type == "anime":
                tasks.append(fetch_mal_anime(smart_query, limit=30))
            elif content_type == "manga":
                tasks.append(fetch_mal_manga(smart_query, limit=30))
            elif content_type == "movies":
                tasks.append(fetch_imdb_movies(smart_query))
            elif content_type in ["web_series", "tv_series"]:
                tasks.append(fetch_imdb_series(smart_query))
        
        # Run all API calls concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results with filtering
        all_items = []
        
        for idx, content_type in enumerate(request.content_types):
            if idx >= len(results):
                break
            
            result = results[idx]
            query_used = content_queries[idx][1] if idx < len(content_queries) else "unknown"
            
            if isinstance(result, Exception):
                print(f"[ERROR] {content_type} ({query_used}): {result}")
                continue
            
            if not result:
                print(f"[INFO] No results for {content_type} with query '{query_used}'")
                continue
            
            print(f"[SUCCESS] {content_type} - Found {len(result)} results for '{query_used}'")
            
            # Format and filter based on content type
            if content_type == "anime":
                for item in result:
                    anime = item.get("node", {})
                    # Filter by minimum rating for quality
                    rating = anime.get("mean", 0)
                    if rating >= 6.0:  # Only include rated anime
                        rec = await format_anime_recommendation(item, exclude_titles)
                        if rec:
                            all_items.append(rec)
            elif content_type == "manga":
                for item in result:
                    manga = item.get("node", {})
                    rating = manga.get("mean", 0)
                    if rating >= 6.0:
                        rec = await format_manga_recommendation(item, exclude_titles)
                        if rec:
                            all_items.append(rec)
            elif content_type == "movies":
                for item in result:
                    try:
                        imdb_rating = float(item.get("imdbRating", "0"))
                        if imdb_rating >= 6.0:  # Only quality movies
                            rec = await format_imdb_recommendation(item, "movies", exclude_titles)
                            if rec:
                                all_items.append(rec)
                    except:
                        pass
            elif content_type in ["web_series", "tv_series"]:
                for item in result:
                    try:
                        imdb_rating = float(item.get("imdbRating", "0"))
                        if imdb_rating >= 6.0:
                            rec = await format_imdb_recommendation(item, "web_series", exclude_titles)
                            if rec:
                                all_items.append(rec)
                    except:
                        pass
        
        if not all_items:
            raise HTTPException(status_code=404, detail=f"No quality recommendations found for: {', '.join(request.content_types)}")
        
        # Shuffle and select
        random.shuffle(all_items)
        selected = all_items[:target_count]
        
        # Add to history
        batch_id = str(__import__('uuid').uuid4())
        for i, item in enumerate(selected):
            item["recommendation_id"] = f"{batch_id}_{i}"
            item["rank"] = i + 1
            
            if request.user_id not in user_history:
                user_history[request.user_id] = []
            user_history[request.user_id].append({
                "content_id": item.get("content_id"),
                "title": item.get("title"),
                "content_type": item.get("content_type"),
                "genres": item.get("genres", []),
                "timestamp": datetime.now().isoformat()
            })
        
        return {
            "status": "success",
            "user_id": request.user_id,
            "batch_id": batch_id,
            "count": len(selected),
            "recommendations": selected,
            "search_queries": [{"type": ct, "query": q} for ct, q in content_queries],
            "powered_by": "Smart Recommendations - MAL API + IMDb API"
        }
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/users/{user_id}/history")
async def get_history(user_id: str):
    """Get user history"""
    return {
        "user_id": user_id,
        "history": user_history.get(user_id, [])
    }


@app.post("/users/{user_id}/watchlater")
async def add_watchlater(user_id: str, content_id: str, title: str, content_type: str):
    """Add to watch later"""
    if user_id not in user_watchlater:
        user_watchlater[user_id] = []
    
    user_watchlater[user_id].append({
        "content_id": content_id,
        "title": title,
        "content_type": content_type,
        "added_at": datetime.now().isoformat()
    })
    
    return {"status": "added"}


@app.get("/users/{user_id}/watchlater")
async def get_watchlater(user_id: str):
    """Get watch later list"""
    return {
        "user_id": user_id,
        "watchlater": user_watchlater.get(user_id, [])
    }


# ==================== Catalog Endpoints ====================

@app.get("/search")
async def search_anime(q: str, limit: int = 25):
    """
    Search for anime by query.
    Results are cached for persistent catalog.
    """
    if not q or len(q) < 2:
        raise HTTPException(status_code=400, detail="Query must be at least 2 characters")
    
    # Check if already cached
    cache_key = f"anime_{q.lower()}_{limit}"
    if cache_key in search_cache:
        print(f"[CACHE HIT] {cache_key}")
        return {
            "query": q,
            "results": search_cache[cache_key],
            "from_cache": True,
            "count": len(search_cache[cache_key])
        }
    
    try:
        # Fetch from MAL API
        results = await fetch_mal_anime(q, limit=limit)
        
        if not results:
            raise HTTPException(status_code=404, detail=f"No anime found for '{q}'")
        
        # Format and cache results
        formatted_results = []
        for item in results:
            rec = await format_anime_recommendation(item, [])
            if rec:
                formatted_results.append(rec)
        
        # Store in cache for persistent catalog
        search_cache[cache_key] = formatted_results
        
        print(f"[CACHE NEW] {cache_key} - {len(formatted_results)} items cached")
        
        return {
            "query": q,
            "results": formatted_results,
            "from_cache": False,
            "count": len(formatted_results)
        }
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/search/cache")
async def get_search_cache():
    """Get all cached search results for persistent catalog"""
    cache_summary = []
    for key, items in search_cache.items():
        query = key.split("_anime_")[1].split("_")[0] if "_anime_" in key else key
        cache_summary.append({
            "query": query,
            "count": len(items),
            "cache_key": key
        })
    
    return {
        "total_searches": len(search_cache),
        "searches": cache_summary,
        "all_items": sum(len(v) for v in search_cache.values())
    }


@app.get("/search/all")
async def get_all_cached_items():
    """Get all items from all cached searches (persistent catalog)"""
    all_items = []
    seen_ids = set()
    
    for items in search_cache.values():
        for item in items:
            item_id = item.get("content_id", "")
            if item_id not in seen_ids:
                all_items.append(item)
                seen_ids.add(item_id)
    
    return {
        "total_items": len(all_items),
        "unique_items": len(seen_ids),
        "items": all_items
    }


# ==================== Catalog Endpoints ====================

@app.get("/catalog/all")
async def get_catalog_all():
    """Get all catalog items (for Catalog page)"""
    try:
        # Fetch a diverse set of recommendations
        tasks = [
            fetch_mal_anime("action", limit=8),
            fetch_mal_manga("fantasy", limit=8),
            fetch_imdb_movies("thriller", 2024),
            fetch_imdb_series("drama"),
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        all_items = []
        
        # Process anime
        if results[0] and not isinstance(results[0], Exception):
            for item in results[0]:
                rec = await format_anime_recommendation(item, [])
                if rec:
                    all_items.append(rec)
        
        # Process manga
        if results[1] and not isinstance(results[1], Exception):
            for item in results[1]:
                rec = await format_manga_recommendation(item, [])
                if rec:
                    all_items.append(rec)
        
        # Process movies
        if results[2] and not isinstance(results[2], Exception):
            for item in results[2]:
                rec = await format_imdb_recommendation(item, "movies", [])
                if rec:
                    all_items.append(rec)
        
        # Process series
        if results[3] and not isinstance(results[3], Exception):
            for item in results[3]:
                rec = await format_imdb_recommendation(item, "web_series", [])
                if rec:
                    all_items.append(rec)
        
        return all_items
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/catalog/{content_type}")
async def get_catalog_by_type(content_type: str):
    """Get catalog items by content type"""
    try:
        query_map = {
            "anime": ("anime", "action"),
            "manga": ("manga", "adventure"),
            "movies": ("movies", "thriller"),
            "web_series": ("web_series", "drama"),
        }
        
        if content_type not in query_map:
            raise HTTPException(status_code=400, detail=f"Unknown content_type: {content_type}")
        
        api_type, query = query_map[content_type]
        all_items = []
        
        if api_type == "anime":
            results = await fetch_mal_anime(query, limit=15)
            for item in results:
                rec = await format_anime_recommendation(item, [])
                if rec:
                    all_items.append(rec)
        elif api_type == "manga":
            results = await fetch_mal_manga(query, limit=15)
            for item in results:
                rec = await format_manga_recommendation(item, [])
                if rec:
                    all_items.append(rec)
        elif api_type == "movies":
            results = await fetch_imdb_movies(query)
            for item in results:
                rec = await format_imdb_recommendation(item, "movies", [])
                if rec:
                    all_items.append(rec)
        elif api_type == "web_series":
            results = await fetch_imdb_series(query)
            for item in results:
                rec = await format_imdb_recommendation(item, "web_series", [])
                if rec:
                    all_items.append(rec)
        
        return all_items
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
