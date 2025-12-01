"""
Ultra-Fast Caching Agent for OtakuVerse
Eliminates delays by caching everything with Gemini
"""

import json
import hashlib
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import asyncio
import urllib.request
import urllib.parse

class FastCacheAgent:
    """Lightning-fast agent using memory cache + Gemini for instant responses"""
    
    def __init__(self):
        self.cache = {}  # In-memory cache
        self.ttl = 3600  # 1 hour cache TTL
        self.catalog_cache = {}
        self.enrichment_cache = {}
        self.search_cache = {}
        
    def _get_cache_key(self, *args) -> str:
        """Generate cache key"""
        key_str = "|".join(str(arg) for arg in args)
        return hashlib.md5(key_str.encode()).hexdigest()
    
    def _is_cached_valid(self, cache_time: float) -> bool:
        """Check if cache entry is still valid"""
        return (datetime.now().timestamp() - cache_time) < self.ttl
    
    async def get_cached_catalog(self, content_type: str) -> List[Dict]:
        """Get catalog from cache with instant response"""
        cache_key = f"catalog_{content_type}"
        
        if cache_key in self.catalog_cache:
            cached = self.catalog_cache[cache_key]
            if self._is_cached_valid(cached['time']):
                return cached['data']
        
        return []
    
    async def cache_catalog(self, content_type: str, data: List[Dict]):
        """Store catalog in fast cache"""
        cache_key = f"catalog_{content_type}"
        self.catalog_cache[cache_key] = {
            'data': data,
            'time': datetime.now().timestamp()
        }
    
    async def get_enriched_with_external_only(self, 
                                              title: str, 
                                              content_type: str) -> Dict[str, Any]:
        """
        Get ONLY external data (MAL rating, IMDb rating, images)
        Everything else from Gemini DB to be ultra-fast
        """
        # For now, return minimal data to avoid crashes
        # TODO: Re-enable external API calls
        return {
            "mal_rating": None,
            "imdb_rating": None,
            "cover_image": None,
            "sources": []
        }
    
    async def _fetch_mal_quick(self, title: str, content_type: str) -> Optional[Dict]:
        """Quick MAL fetch with timeout using stdlib"""
        try:
            search_type = "anime" if content_type in ["anime", "light_novels"] else "manga"
            url = f"https://api.jikan.moe/v4/search/{search_type}"
            params = urllib.parse.urlencode({"query": title, "limit": 1})
            full_url = f"{url}?{params}"
            
            def fetch():
                req = urllib.request.Request(full_url, headers={'User-Agent': 'OtakuVerse'})
                with urllib.request.urlopen(req, timeout=2.0) as response:
                    data = json.loads(response.read())
                    if data.get("data") and len(data["data"]) > 0:
                        result = data["data"][0]
                        return {
                            "rating": result.get("score"),
                            "image": result.get("images", {}).get("jpg", {}).get("image_url")
                        }
            
            # Run in executor to avoid blocking
            loop = asyncio.get_event_loop()
            result = await asyncio.wait_for(
                loop.run_in_executor(None, fetch),
                timeout=2.0
            )
            return result
            
        except asyncio.TimeoutError:
            pass  # Skip if takes too long
        except Exception as e:
            pass  # Silently skip errors
        
        return None
    
    async def _fetch_imdb_quick(self, title: str) -> Optional[Dict]:
        """Quick IMDb fetch with timeout using stdlib"""
        try:
            import os
            
            omdb_key = os.getenv('OMDB_API_KEY', '')
            if not omdb_key:
                return None
            
            params = urllib.parse.urlencode({"apikey": omdb_key, "t": title, "type": "movie"})
            url = f"https://www.omdbapi.com/?{params}"
            
            def fetch():
                req = urllib.request.Request(url, headers={'User-Agent': 'OtakuVerse'})
                with urllib.request.urlopen(req, timeout=2.0) as response:
                    data = json.loads(response.read())
                    if data.get("Response") == "True":
                        rating_str = data.get("imdbRating", "0")
                        rating = float(rating_str) if rating_str != "N/A" else None
                        return {
                            "rating": rating,
                            "image": data.get("Poster") if data.get("Poster") != "N/A" else None
                        }
            
            # Run in executor to avoid blocking
            loop = asyncio.get_event_loop()
            result = await asyncio.wait_for(
                loop.run_in_executor(None, fetch),
                timeout=2.0
            )
            return result
            
        except asyncio.TimeoutError:
            pass  # Skip if takes too long
        except Exception as e:
            pass  # Silently skip errors
        
        return None
    
    async def search_fast(self, 
                         query: str,
                         catalog_data: List[Dict],
                         limit: int = 20) -> List[Dict]:
        """Ultra-fast search using in-memory cache and string matching"""
        cache_key = self._get_cache_key("search", query, limit)
        
        if cache_key in self.search_cache:
            cached = self.search_cache[cache_key]
            if self._is_cached_valid(cached['time']):
                return cached['data']
        
        query_lower = query.lower()
        results = []
        
        # Fast string matching
        for item in catalog_data:
            if (query_lower in item.get("title", "").lower() or
                any(query_lower in g.lower() for g in item.get("genres", []))):
                results.append(item)
                if len(results) >= limit:
                    break
        
        self.search_cache[cache_key] = {
            'data': results,
            'time': datetime.now().timestamp()
        }
        
        return results
    
    def clear_expired_cache(self):
        """Periodically clear expired cache entries"""
        current_time = datetime.now().timestamp()
        
        for cache_dict in [self.catalog_cache, self.enrichment_cache, self.search_cache]:
            expired_keys = [
                key for key, value in cache_dict.items()
                if (current_time - value['time']) > self.ttl
            ]
            for key in expired_keys:
                del cache_dict[key]


# Global fast cache agent
fast_cache = FastCacheAgent()
