import httpx
import os
from typing import Optional, Dict, Any
import asyncio
from functools import lru_cache

class ImageAndRatingHandler:
    """Handles image and rating fetching from external sources"""

    def __init__(self):
        self.omdb_key = os.getenv('OMDB_API_KEY', '2d9726cf')
        self.jikan_base = "https://api.jikan.moe/v4"
        self.omdb_base = "https://www.omdbapi.com"
        self.image_cache = {}
        self.rating_cache = {}
        self.timeout = 15.0

    async def get_mal_data(self, title: str, content_type: str) -> Optional[Dict[str, Any]]:
        """Fetch data from MyAnimeList via Jikan API"""
        try:
            search_type = "anime" if content_type in ["anime", "light_novels"] else "manga"
            url = f"{self.jikan_base}/search/{search_type}"
            params = {"query": title, "limit": 1}
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                data = response.json()
            
            if data.get("data") and len(data["data"]) > 0:
                result = data["data"][0]
                return {
                    "title": result.get("title"),
                    "poster_url": result.get("images", {}).get("jpg", {}).get("image_url"),
                    "rating": result.get("score"),
                    "rating_count": result.get("scored_by"),
                    "description": result.get("synopsis"),
                    "genres": [g["name"] for g in result.get("genres", [])],
                    "year": result.get("year"),
                }
            return None
        except Exception as e:
            print(f"Warning: Error fetching MAL data for '{title}': {e}")
            return None

    async def get_imdb_data(self, title: str, year: Optional[int] = None) -> Optional[Dict[str, Any]]:
        """Fetch data from IMDb via OMDb API"""
        if not self.omdb_key:
            print("Warning: OMDB_API_KEY not configured")
            return None
        
        try:
            url = f"{self.omdb_base}/"
            params = {
                "apikey": self.omdb_key,
                "t": title,
                "type": "movie"
            }
            if year:
                params["y"] = year
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                data = response.json()
            
            if data.get("Response") == "True" and data.get("Poster") != "N/A":
                return {
                    "title": data.get("Title"),
                    "poster_url": data.get("Poster"),
                    "rating": float(data.get("imdbRating", 0)) if data.get("imdbRating") != "N/A" else None,
                    "rating_count": data.get("imdbVotes"),
                    "description": data.get("Plot"),
                    "genres": [g.strip() for g in data.get("Genre", "").split(",")],
                    "year": int(data.get("Year", 0)),
                    "director": data.get("Director"),
                }
            return None
        except Exception as e:
            print(f"Warning: Error fetching IMDb data for '{title}': {e}")
            return None

    async def get_ratings(self, title: str, content_type: str) -> Optional[Dict[str, Any]]:
        """Get ratings from multiple sources"""
        cache_key = f"{title}-{content_type}"
        
        if cache_key in self.rating_cache:
            return self.rating_cache[cache_key]

        rating_data = {
            "sources": [],
            "imdb_rating": None,
            "mal_rating": None,
        }

        # Try both sources in parallel
        tasks = []
        
        if content_type in ["anime", "manga", "light_novels", "manhwa"]:
            tasks.append(self.get_mal_data(title, content_type))
        
        if content_type in ["movies", "web_series", "comics", "games"]:
            tasks.append(self.get_imdb_data(title))

        if tasks:
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for result in results:
                if isinstance(result, dict) and "rating" in result and result["rating"]:
                    if content_type in ["anime", "manga", "light_novels", "manhwa"]:
                        rating_data["mal_rating"] = result["rating"]
                        rating_data["sources"].append("MAL")
                    else:
                        rating_data["imdb_rating"] = result["rating"]
                        rating_data["sources"].append("IMDb")

        self.rating_cache[cache_key] = rating_data
        return rating_data

    async def get_enriched_item(self, title: str, content_type: str) -> Dict[str, Any]:
        """Get enriched item data with images and ratings"""
        cache_key = f"enriched-{title}-{content_type}"
        
        if cache_key in self.image_cache:
            return self.image_cache[cache_key]

        enriched_data = {
            "title": title,
            "content_type": content_type,
            "images": {},
            "ratings": {},
            "metadata": {}
        }

        # Fetch from appropriate source
        if content_type in ["anime", "manga", "light_novels", "manhwa"]:
            mal_data = await self.get_mal_data(title, content_type)
            if mal_data:
                enriched_data["images"]["poster_url"] = mal_data.get("poster_url")
                enriched_data["ratings"]["mal_rating"] = mal_data.get("rating")
                enriched_data["metadata"]["description"] = mal_data.get("description")
                enriched_data["metadata"]["genres"] = mal_data.get("genres")
                enriched_data["metadata"]["year"] = mal_data.get("year")
        else:
            imdb_data = await self.get_imdb_data(title)
            if imdb_data:
                enriched_data["images"]["poster_url"] = imdb_data.get("poster_url")
                enriched_data["ratings"]["imdb_rating"] = imdb_data.get("rating")
                enriched_data["metadata"]["description"] = imdb_data.get("description")
                enriched_data["metadata"]["genres"] = imdb_data.get("genres")
                enriched_data["metadata"]["year"] = imdb_data.get("year")
                enriched_data["metadata"]["director"] = imdb_data.get("director")

        self.image_cache[cache_key] = enriched_data
        return enriched_data

    def clear_cache(self):
        """Clear all caches"""
        self.image_cache.clear()
        self.rating_cache.clear()

# Create singleton instance
image_rating_handler = ImageAndRatingHandler()
