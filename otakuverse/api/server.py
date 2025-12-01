from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import uuid
from datetime import datetime
import os
import sys
import json

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from history_agent.db import HistoryDatabase
from catalog_agent.agent import CatalogManager

# Mood mapping from frontend to anime moods
MOOD_MAPPING = {
    'happy': ['fun', 'wholesome', 'heartwarming', 'inspiring'],
    'sad': ['emotional', 'dark', 'intense', 'melancholic'],
    'excited': ['thrilling', 'epic', 'intense', 'cool'],
    'calm': ['wholesome', 'heartwarming', 'beautiful', 'peaceful'],
    'melancholic': ['emotional', 'dark', 'thoughtful', 'intense'],
    'adventurous': ['epic', 'thrilling', 'intense', 'cool'],
    'nostalgic': ['beautiful', 'emotional', 'wholesome', 'heartwarming'],
    'introspective': ['thoughtful', 'emotional', 'mind-bending', 'dark']
}

# Initialize FastAPI app
app = FastAPI(
    title="OtakuVerse API",
    description="Multi-agent entertainment recommendation backend - ANIME FOCUSED",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
db = HistoryDatabase()
catalog_manager = CatalogManager()


async def generate_explanation(title: str, content_type: str, genres: List[str], mood: List[str]) -> str:
    """Generate explanation for recommendation."""
    try:
        genre_str = ", ".join(genres) if genres else "mixed"
        mood_str = ", ".join(mood) if mood else "various"
        return f"This {content_type} with {genre_str} genres matches your {mood_str} preference perfectly."
    except Exception as e:
        print(f"Error generating explanation: {e}")
        return f"This {content_type} matches your preferences."

# Pydantic models
class UserCreate(BaseModel):
    user_id: str
    preferences: Optional[dict] = None


class RecommendationRequest(BaseModel):
    user_id: str
    genres: Optional[List[str]] = None
    moods: Optional[List[str]] = None
    content_types: List[str]  # Required: user must specify which types


class ContentHistoryEntry(BaseModel):
    content_id: str
    content_type: str
    title: str
    rating: Optional[float] = None
    notes: str = ""


class RecommendationResponse(BaseModel):
    recommendation_id: str
    content_id: str
    title: str
    content_type: str
    genres: List[str]
    mood: List[str]
    rating: float
    description: str
    explanation: str
    rank: int


# Routes

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "OtakuVerse Backend API",
        "version": "1.0.0",
        "description": "Multi-agent entertainment recommendation system - ANIME FOCUSED"
    }


@app.post("/users")
async def create_user(user: UserCreate):
    """Create a new user or get existing user."""
    db.create_user(user.user_id, user.preferences)
    return {
        "user_id": user.user_id,
        "message": "User created or updated",
        "created_at": datetime.now().isoformat()
    }


@app.get("/users/{user_id}")
async def get_user(user_id: str):
    """Get user profile and preferences."""
    user = db.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.get("/users/{user_id}/history")
async def get_user_history(user_id: str, content_type: Optional[str] = None):
    """Get user's content history."""
    history = db.get_user_history(user_id, content_type)
    return {
        "user_id": user_id,
        "count": len(history),
        "history": history
    }


@app.post("/users/{user_id}/history")
async def add_to_history(user_id: str, entry: ContentHistoryEntry):
    """Add content to user's history."""
    # Ensure user exists
    if not db.get_user(user_id):
        db.create_user(user_id)
    
    db.add_to_history(
        user_id, 
        entry.content_id, 
        entry.content_type, 
        entry.title, 
        entry.rating, 
        entry.notes
    )
    
    return {
        "user_id": user_id,
        "message": "Content added to history",
        "content": entry
    }


@app.get("/content-types")
async def get_content_types():
    """Get all available content types."""
    return {
        "content_types": [
            "anime",
            "movies", 
            "web_series",
            "manga",
            "manhwa",
            "comics",
            "light_novels",
            "novels",
            "games"
        ]
    }


@app.post("/recommendations")
async def get_recommendations(request: RecommendationRequest):
    """Get recommendations for a user."""
    
    # Ensure user exists
    user = db.get_user(request.user_id)
    if not user:
        db.create_user(request.user_id)
    
    # Validate that content_types are provided
    if not request.content_types:
        raise HTTPException(
            status_code=400, 
            detail="content_types must be specified"
        )
    
    # Get user's consumed content
    consumed_ids = db.get_consumed_ids(request.user_id)
    
    # Search catalog
    try:
        # Map frontend moods to anime moods
        anime_moods = []
        if request.moods:
            for mood in request.moods:
                mood_lower = mood.lower()
                if mood_lower in MOOD_MAPPING:
                    anime_moods.extend(MOOD_MAPPING[mood_lower])
                else:
                    anime_moods.append(mood_lower)
            # Remove duplicates while preserving order
            anime_moods = list(dict.fromkeys(anime_moods))
            print(f"Frontend Moods: {request.moods} → Anime Moods: {anime_moods}")
        
        if request.genres and anime_moods:
            results = catalog_manager.search_by_genre_and_mood(
                request.genres,
                anime_moods,
                request.content_types
            )
        elif request.genres:
            results = catalog_manager.search_by_genres(
                request.genres,
                request.content_types
            )
        elif anime_moods:
            results = catalog_manager.search_by_mood(
                anime_moods,
                request.content_types
            )
        else:
            results = catalog_manager.get_by_type(request.content_types)
        
        # Filter out consumed content
        filtered_results = catalog_manager.filter_out_consumed(results, consumed_ids)
        
        # Limit to top 10 recommendations
        recommendations = filtered_results[:10]
        
        # Format response
        batch_id = str(uuid.uuid4())
        formatted_recommendations = []
        
        for i, rec in enumerate(recommendations):
            title = rec.get("title", "")
            content_type = rec.get("content_type", "")
            genres = rec.get("genres", [])
            mood = rec.get("mood", [])
            
            # Generate explanation
            explanation = await generate_explanation(title, content_type, genres, mood)
            
            formatted_rec = {
                "recommendation_id": f"{batch_id}_{i}",
                "content_id": rec.get("id"),
                "title": title,
                "content_type": content_type,
                "genres": genres,
                "mood": mood,
                "rating": rec.get("rating", 0),
                "description": rec.get("description"),
                "explanation": explanation,
                "rank": i + 1,
                "mal_score": None,
                "imdb_score": None,
                "cover_image": None,
                "external_metadata": {}
            }
            
            formatted_recommendations.append(formatted_rec)
            
            # Save to database
            db.save_recommendation(
                request.user_id,
                batch_id,
                rec.get("id"),
                content_type,
                title,
                explanation,
                i + 1
            )
        
        return {
            "user_id": request.user_id,
            "session_id": batch_id,
            "criteria": {
                "genres": request.genres,
                "moods": request.moods,
                "content_types": request.content_types
            },
            "count": len(formatted_recommendations),
            "recommendations": formatted_recommendations
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating recommendations: {str(e)}"
        )


@app.get("/recommendations/{user_id}")
async def get_user_recommendations(user_id: str):
    """Get user's past recommendations."""
    recommendations = db.get_recommendations(user_id)
    return {
        "user_id": user_id,
        "count": len(recommendations),
        "recommendations": recommendations
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/catalog/all")
async def get_all_catalog():
    """Get all catalog items."""
    try:
        all_items = []
        for content_type, catalog in catalog_manager.catalogs.items():
            for item in catalog:
                enriched_item = {
                    "id": item.get("id"),
                    "title": item.get("title"),
                    "content_type": content_type,
                    "genres": item.get("genres", []),
                    "mood": item.get("mood", []),
                    "description": item.get("description"),
                    "rating_score": item.get("rating", 0),
                    "mal_score": None,
                    "imdb_score": None,
                    "cover_image": None,
                    "explanation": f"Part of our {content_type} collection",
                    "user_rating": 0
                }
                all_items.append(enriched_item)
        
        return all_items
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading catalog: {str(e)}")


@app.get("/catalog/{content_type}")
async def get_catalog_by_type(content_type: str):
    """Get catalog items by content type."""
    try:
        content_type_key = content_type.replace('-', '_').lower()
        
        if content_type_key not in catalog_manager.catalogs:
            raise HTTPException(status_code=404, detail=f"Content type {content_type} not found")
        
        catalog = catalog_manager.catalogs[content_type_key]
        enriched_items = []
        
        for item in catalog:
            enriched_item = {
                "id": item.get("id"),
                "title": item.get("title"),
                "content_type": content_type_key,
                "genres": item.get("genres", []),
                "mood": item.get("mood", []),
                "description": item.get("description"),
                "rating_score": item.get("rating", 0),
                "mal_score": None,
                "imdb_score": None,
                "cover_image": None,
                "explanation": f"Part of our {content_type_key} collection",
                "user_rating": 0
            }
            enriched_items.append(enriched_item)
        
        return enriched_items
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading catalog: {str(e)}")


@app.get("/search")
async def search(q: str, limit: int = 25):
    """Search across all catalogs by title."""
    try:
        query = q.lower().strip()
        if not query:
            raise HTTPException(status_code=400, detail="Search query cannot be empty")
        
        results = []
        
        # Search through all content types
        for content_type, catalog in catalog_manager.catalogs.items():
            for item in catalog:
                title = item.get("title", "").lower()
                if query in title or title.startswith(query):
                    results.append({
                        "content_id": item.get("id"),
                        "title": item.get("title"),
                        "content_type": content_type,
                        "genres": item.get("genres", []),
                        "description": item.get("description", ""),
                        "mal_score": item.get("rating", 0),
                        "cover_image": None,
                        "episodes": item.get("episodes"),
                        "status": item.get("status")
                    })
        
        # Sort by relevance (exact match first, then starts with, then contains)
        def sort_key(item):
            title = item["title"].lower()
            if title == query:
                return (0, title)
            elif title.startswith(query):
                return (1, title)
            else:
                return (2, title)
        
        results.sort(key=sort_key)
        
        return {
            "query": q,
            "results": results[:limit],
            "from_cache": False,
            "count": len(results[:limit])
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search error: {str(e)}")


@app.on_event("shutdown")
async def shutdown_event():
    """Close database connection on shutdown."""
    db.close()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
