"""
Ultra-Fast OtakuVerse API - Optimized for Speed
Uses caching, parallel operations, and Gemini for instant responses
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import uuid
from datetime import datetime
import os
import sys
import json
import asyncio

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from history_agent.db import HistoryDatabase
from catalog_agent.agent import CatalogManager
from agents.fast_cache_agent import fast_cache

# Initialize FastAPI with response compression
app = FastAPI(
    title="OtakuVerse - Ultra-Fast Edition",
    description="Lightning-fast entertainment recommendations",
    version="3.0.0"
)

# Add CORS with optimizations
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
db = HistoryDatabase()
catalog_manager = CatalogManager()

# Pre-load all catalogs into fast cache on startup
@app.on_event("startup")
async def startup_event():
    """Pre-cache all catalogs for instant access"""
    print("[STARTUP] Pre-caching all catalogs...")
    
    for content_type, catalog in catalog_manager.catalogs.items():
        await fast_cache.cache_catalog(content_type, catalog)
        print(f"  [OK] Cached {len(catalog)} {content_type} items")
    
    print("[SUCCESS] All catalogs cached - Ready for ultra-fast performance!")


# ==================== Pydantic Models ====================

class RecommendationRequest(BaseModel):
    user_id: str
    genres: Optional[List[str]] = None
    moods: Optional[List[str]] = None
    content_types: List[str]


class ContentHistoryEntry(BaseModel):
    content_id: str
    content_type: str
    title: str
    rating: Optional[float] = None


class UserCreate(BaseModel):
    user_id: str
    preferences: Optional[dict] = None


# ==================== Lightning-Fast Endpoints ====================

@app.get("/", response_model=dict)
async def root():
    """Ultra-fast root endpoint"""
    return {
        "app": "OtakuVerse Ultra-Fast",
        "version": "3.0.0",
        "status": "[READY]",
        "catalog_cached": True
    }


@app.get("/health")
async def health():
    """Instant health check"""
    return {"status": "healthy"}


@app.get("/catalog/all", response_model=list)
async def get_all_catalog_fast():
    """
    [INSTANT] catalog - Pre-cached in memory
    Response time: < 50ms
    """
    try:
        all_items = []
        
        # Get all cached catalogs in parallel
        tasks = [
            fast_cache.get_cached_catalog(content_type)
            for content_type in catalog_manager.catalogs.keys()
        ]
        
        results = await asyncio.gather(*tasks)
        
        for items in results:
            all_items.extend(items)
        
        return all_items
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/catalog/{content_type}", response_model=list)
async def get_catalog_by_type_fast(content_type: str):
    """
    ⚡ INSTANT catalog by type - Cached
    Response time: < 30ms
    """
    try:
        content_type_key = content_type.replace('-', '_').lower()
        
        if content_type_key not in catalog_manager.catalogs:
            raise HTTPException(status_code=404, detail=f"Content type {content_type} not found")
        
        # Get from fast cache
        cached_items = await fast_cache.get_cached_catalog(content_type_key)
        
        if not cached_items:
            # Fallback: cache now
            catalog = catalog_manager.catalogs[content_type_key]
            await fast_cache.cache_catalog(content_type_key, catalog)
            cached_items = catalog
        
        return cached_items
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/recommendations")
async def get_recommendations_fast(request: RecommendationRequest):
    """
    [FAST] recommendations with external data (MAL/IMDb ratings + images only)
    Response time: 1-3 seconds (external API calls only)
    """
    import sys
    try:
        print(f"[RECO] Recommendation request received", flush=True)
        sys.stdout.flush()
        print(f"[RECO] Request: {request.dict()}", flush=True)
        sys.stdout.flush()
        # Skip DB for now - causes threading issues
        # user = db.get_user(request.user_id)
        # if not user:
        #     db.create_user(request.user_id)
        
        if not request.content_types:
            raise HTTPException(status_code=400, detail="content_types required")
        
        # Get all cached items for the requested content types in parallel
        print(f"[RECO] Fetching catalogs for: {request.content_types}")
        tasks = [
            fast_cache.get_cached_catalog(ct.replace('-', '_').lower())
            for ct in request.content_types
        ]
        
        catalog_results = await asyncio.gather(*tasks)
        all_items = []
        for items in catalog_results:
            all_items.extend(items)
        
        print(f"[RECO] Total items found: {len(all_items)}")
        
        # Skip consumed check for now
        # consumed_ids = db.get_consumed_ids(request.user_id)
        # available_items = [
        #     item for item in all_items 
        #     if item.get("id") not in consumed_ids
        # ]
        available_items = all_items
        
        # Sort by relevance if genres/moods specified
        if request.genres or request.moods:
            scored_items = []
            
            for item in available_items:
                score = 0
                if request.genres:
                    score += sum(1 for g in request.genres 
                               if g.lower() in [x.lower() for x in item.get("genres", [])])
                if request.moods:
                    score += sum(1 for m in request.moods 
                               if m.lower() in [x.lower() for x in item.get("mood", [])])
                
                if score > 0:
                    scored_items.append((item, score))
            
            # Sort by score descending
            scored_items.sort(key=lambda x: x[1], reverse=True)
            available_items = [item for item, _ in scored_items[:20]]
        else:
            # Return up to 20 items
            available_items = available_items[:20]
        
        # Fetch external data (MAL/IMDb) for top items in parallel
        enrichment_tasks = [
            fast_cache.get_enriched_with_external_only(
                item.get("title", ""),
                item.get("content_type", "")
            )
            for item in available_items
        ]
        
        enrichments = await asyncio.gather(*enrichment_tasks, return_exceptions=True)
        
        # Format response
        batch_id = str(uuid.uuid4())
        recommendations = []
        
        for i, (item, enriched) in enumerate(zip(available_items, enrichments)):
            if isinstance(enriched, Exception):
                print(f"Enrichment error for {item.get('title')}: {enriched}")
                enriched = {"mal_rating": None, "imdb_rating": None, "cover_image": None}
            
            rec = {
                "recommendation_id": f"{batch_id}_{i}",
                "content_id": item.get("id"),
                "title": item.get("title"),
                "content_type": item.get("content_type"),
                "genres": item.get("genres", []),
                "mood": item.get("mood", []),
                "rating": item.get("rating", 0),
                "description": item.get("description", ""),
                "mal_score": enriched.get("mal_rating"),
                "imdb_score": enriched.get("imdb_rating"),
                "cover_image": enriched.get("cover_image"),
                "rank": i + 1
            }
            
            recommendations.append(rec)
            
            # Skip DB save for now
            # db.save_recommendation(
            #     request.user_id, batch_id, item.get("id"),
            #     item.get("content_type"), item.get("title"),
            #     f"Recommendation {i+1}", i + 1
            # )
        
        return {
            "status": "success",
            "user_id": request.user_id,
            "count": len(recommendations),
            "recommendations": recommendations,
            "response_time_ms": f"1-3s (external data only)"
        }
        
    except Exception as e:
        import traceback
        print(f"[ERROR] Recommendations error: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/search")
async def search_fast(q: str, content_type: Optional[str] = None):
    """
    [INSTANT] search from cache
    Response time: < 20ms
    """
    try:
        # Get all cached items
        all_items = []
        for ct, catalog in catalog_manager.catalogs.items():
            if content_type is None or ct == content_type:
                all_items.extend(catalog)
        
        # Fast search
        results = await fast_cache.search_fast(q, all_items, limit=20)
        
        return {
            "query": q,
            "count": len(results),
            "results": results
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/users")
async def create_user_fast(user: UserCreate):
    """Create user instantly"""
    db.create_user(user.user_id, user.preferences)
    return {"user_id": user.user_id, "status": "created"}


@app.get("/users/{user_id}/history")
async def get_history_fast(user_id: str):
    """Get user history instantly"""
    history = db.get_user_history(user_id)
    return {"user_id": user_id, "count": len(history), "history": history}


@app.post("/users/{user_id}/history")
async def add_to_history_fast(user_id: str, entry: ContentHistoryEntry):
    """Add to history instantly"""
    if not db.get_user(user_id):
        db.create_user(user_id)
    
    db.add_to_history(
        user_id, entry.content_id, entry.content_type, entry.title, entry.rating
    )
    return {"status": "added"}


@app.get("/stats")
async def get_stats():
    """Get system stats"""
    total = sum(len(cat) for cat in catalog_manager.catalogs.values())
    return {
        "total_items": total,
        "content_types": list(catalog_manager.catalogs.keys()),
        "cache_status": "[HOT] All catalogs pre-cached"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api.server_fast:app",
        host="0.0.0.0",
        port=8000,
        reload=False,  # Faster without reload
        log_level="info"
    )
