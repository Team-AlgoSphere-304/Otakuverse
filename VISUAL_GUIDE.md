# OtakuVerse Real Data Integration - Visual Guide

## 🎬 Data Flow Visualization

### Simple Version
```
User 
  ↓ Selects Preferences
Backend Catalog Search
  ↓
Get Real Scores + Images
  ├─ Jikan API → MAL Score
  ├─ OMDb API → IMDb Score
  └─ Gemini → AI Explanation
  ↓
Frontend Display
  ✅ Real Scores
  ✅ Real Images
  ✅ AI Text
```

### Detailed Version

```
┌─────────────────────────────────────────────────────────────┐
│                    USER INTERFACE                           │
│  http://localhost:3001                                      │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Select: Anime, Horror, Intense                      │   │
│  │ [Generate Recommendations Button]                   │   │
│  └──────────────────────────────────────────────────────┘   │
└──────────────────────────┬────────────────────────────────────┘
                           │ POST /recommendations
                           ▼
        ┌──────────────────────────────────────┐
        │     BACKEND API (FastAPI)            │
        │  http://localhost:8000               │
        │  ┌──────────────────────────────┐    │
        │  │ Search Catalogs              │    │
        │  │ (anime.json, movies.json)    │    │
        │  └──────────────────────────────┘    │
        └──────────────┬───────────────────────┘
                       │
        ┌──────────────┴──────────────────────┐
        │                                     │
   ┌────▼──────┐                      ┌───────▼────┐
   │ For each  │                      │  For each  │
   │  Anime    │                      │   Movie    │
   └────┬──────┘                      └───────┬────┘
        │                                     │
    ┌───▼─────────────────┐          ┌────────▼──────────┐
    │   Jikan API Call    │          │   OMDb API Call   │
    │  (MyAnimeList)      │          │                   │
    │                     │          │ api.omdbapi.com   │
    │ Query: "Attack on   │          │                   │
    │         Titan"      │          │ Query: "Inception"│
    │                     │          │                   │
    │ Returns:            │          │ Returns:          │
    │ • score: 9.09       │          │ • imdbRating: 8.8 │
    │ • poster_url: ...   │          │ • Poster: ...     │
    │ • genres: [...]     │          │ • Plot: ...       │
    │ • synopsis: ...     │          │ • Director: ...   │
    └─────┬───────────────┘          └────────┬──────────┘
          │                                   │
          └───────────────┬───────────────────┘
                          │
                    ┌─────▼──────────────┐
                    │  Gemini API Call   │
                    │  (Google)          │
                    │                    │
                    │ Prompt: Generate   │
                    │ explanation for    │
                    │ why this rec       │
                    │ matches user       │
                    │                    │
                    │ Returns:           │
                    │ explanation: "..." │
                    └─────┬──────────────┘
                          │
           ┌──────────────▼───────────────┐
           │   Combine All Real Data      │
           │                              │
           │ {                            │
           │   "title": "Attack on Titan",│
           │   "mal_score": 9.09,        │ ✨ REAL
           │   "imdb_score": null,       │ ✨ REAL
           │   "cover_image": "...",     │ ✨ REAL
           │   "explanation": "..."      │ ✨ REAL
           │ }                            │
           └──────────────┬───────────────┘
                          │ JSON Response
                          ▼
        ┌──────────────────────────────────┐
        │     FRONTEND (React)              │
        │                                  │
        │  Parse real data                 │
        │  Transform for display           │
        │  Render cards                    │
        └──────────────┬───────────────────┘
                       │
    ┌──────────────────▼──────────────────┐
    │     RECOMMENDATION CARD              │
    │  ┌──────────────────────────────┐   │
    │  │                              │   │
    │  │  [Real Poster Image]         │   │
    │  │  from MAL CDN ✨             │   │
    │  │                              │   │
    │  │   Attack on Titan            │   │
    │  │   MAL 9.09 ✨  [Blue Badge]  │   │
    │  │   [More genres...]           │   │
    │  │                              │   │
    │  │ [Why?] [Watch Later]         │   │
    │  └──────────────────────────────┘   │
    │                                      │
    │  [Click "Why?"]                      │
    │           │                          │
    │           ▼                          │
    │  ┌──────────────────────────────┐   │
    │  │  AI ANALYSIS (Card Back)     │   │
    │  │                              │   │
    │  │  "This anime combines        │   │
    │  │   intense action with        │   │
    │  │   complex character arcs,    │   │
    │  │   matching your preference   │   │
    │  │   for psychological depth."  │   │ ✨ GEMINI AI
    │  │                              │   │
    │  │  Powered by Gemini ✨       │   │
    │  └──────────────────────────────┘   │
    └─────────────────────────────────────┘
```

---

## 🔄 Caching Strategy

```
First Request for "Attack on Titan"
│
├─ NOT in cache
│  ├─ Call Jikan API → Get data
│  ├─ Call Gemini API → Get explanation
│  └─ Store in cache
│
└─ Time: ~500ms ⏱️

Second Request for "Attack on Titan"
│
├─ FOUND in cache! ✨
│  └─ Return cached data immediately
│
└─ Time: ~10ms ⚡
```

---

## 🎯 API Integration Points

```
┌─────────────────────────────────────────────────────┐
│                  Backend Server                     │
│              Port: 8000 (Uvicorn)                   │
│                                                     │
│  /recommendations endpoint                         │
│  ├─ Input: Genres, Moods, Content Types           │
│  │                                                 │
│  ├─ Search: Local JSON catalogs                   │
│  │                                                 │
│  ├─ Enrich: Call external APIs                    │
│  │   ├─ Jikan API                                 │
│  │   ├─ OMDb API                                  │
│  │   └─ Gemini API                                │
│  │                                                 │
│  └─ Output: Enriched recommendations              │
│             with real scores & images             │
│                                                     │
└─────────────────────────────────────────────────────┘
         │
         │ (HTTP + JSON)
         │
┌────────▼────────────────────────────────────────────┐
│             Frontend Application                    │
│              Port: 3001 (Vite)                      │
│                                                     │
│  ├─ API Service transforms data                    │
│  ├─ Image Service fetches images                   │
│  ├─ Gemini Service handles explanations            │
│  └─ Components display real data                   │
│                                                     │
│  Result: User sees real MAL/IMDb scores           │
│         and real poster images!                    │
└──────────────────────────────────────────────────────┘
```

---

## 📊 Real Data Sources Comparison

```
┌─────────────────────────────────────────────────────┐
│           Anime & Manga Data                        │
├─────────────────────────────────────────────────────┤
│ Source: Jikan API (MyAnimeList wrapper)             │
│ URL: https://api.jikan.moe/v4/...                  │
│                                                     │
│ Provides:                                           │
│ ✅ MAL Score (0-10)                                │
│ ✅ Poster Image (HTTPS from MAL CDN)               │
│ ✅ Genres (array)                                  │
│ ✅ Synopsis (text)                                 │
│ ✅ Release Year                                    │
│ ✅ Rating Count                                    │
│                                                     │
│ Rate Limit: 10 requests/second (free)              │
│ Cache: Backend session cache                       │
│                                                     │
│ Example Response:                                   │
│ {                                                  │
│   "data": [{                                       │
│     "title": "Attack on Titan",                    │
│     "score": 9.09,                                 │
│     "images": {                                    │
│       "jpg": {                                     │
│         "image_url": "https://..."                 │
│       }                                            │
│     }                                              │
│   }]                                               │
│ }                                                  │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│         Movies & TV Series Data                     │
├─────────────────────────────────────────────────────┤
│ Source: OMDb API (IMDb data)                        │
│ URL: https://www.omdbapi.com/                      │
│ Key: 2d9726cf                                      │
│                                                     │
│ Provides:                                           │
│ ✅ IMDb Rating (0-10)                              │
│ ✅ Poster Image (HTTPS from IMDb CDN)              │
│ ✅ Genres (comma-separated)                        │
│ ✅ Plot (text)                                     │
│ ✅ Release Year                                    │
│ ✅ Director/Writer                                 │
│ ✅ IMDb Vote Count                                 │
│                                                     │
│ Rate Limit: 100 requests/day (free tier)           │
│ Cache: Frontend Map cache + backend                │
│                                                     │
│ Example Response:                                   │
│ {                                                  │
│   "Title": "Inception",                            │
│   "imdbRating": "8.8",                             │
│   "Poster": "https://...",                         │
│   "Plot": "A skilled thief...",                    │
│   "Director": "Christopher Nolan",                 │
│   "Year": "2010"                                   │
│ }                                                  │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│         AI Explanations & Analysis                  │
├─────────────────────────────────────────────────────┤
│ Source: Google Gemini API                           │
│ URL: https://generativelanguage.googleapis.com/...  │
│ Key: AIzaSyDpFTtjNV86sSxPrZWjByhqWSgyl_ARHs        │
│                                                     │
│ Provides:                                           │
│ ✅ Personalized explanations                       │
│ ✅ Match analysis                                  │
│ ✅ Key recommendation reasons                      │
│ ✅ Natural language responses                      │
│                                                     │
│ Rate Limit: 50 requests/minute (your quota)        │
│ Cache: Frontend sessionStorage                     │
│                                                     │
│ Example Output:                                     │
│ "This anime combines intense action with complex   │
│  psychological themes, perfectly matching your     │
│  preferences for thought-provoking entertainment   │
│  with spectacular animation."                      │
└─────────────────────────────────────────────────────┘
```

---

## 🎨 Card Display Layout

### Front of Card (Default View)
```
┌──────────────────────────────────┐
│  [Content Type Badge]            │ Top Left: Anime/Movie tag
│  MAL 9.09  IMDb 8.8              │ Top Right: Real scores
│                                  │
│   [Real Poster Image]            │ Center: Official image
│   (from MAL/IMDb CDN)            │ (from official source)
│                                  │
│  Attack on Titan                 │ Title
│                                  │
│  MAL 9.09  | Action, Drama       │ Real score + genres
│                                  │
│  [Flip for Analysis] [Save]      │ Buttons on hover
└──────────────────────────────────┘
   ^                                  
   └─ Shows REAL data, not mock!
```

### Back of Card (On Flip)
```
┌──────────────────────────────────┐
│  AI ANALYSIS                     │ Header
│                                  │
│  "This anime combines intense    │ Gemini-generated
│   action with complex character  │ explanation
│   development, matching your     │ (personalized)
│   preference for psychological   │
│   depth and epic storytelling."  │
│                                  │
│  Synopsis                        │
│  "Humanity fights for survival   │ Real metadata
│   against giant humanoid         │ from APIs
│   creatures..."                  │
│                                  │
│  [Back to Card]                  │
└──────────────────────────────────┘
```

---

## 🚀 Request/Response Flow

### Request from Frontend
```json
{
  "user_id": "user-123",
  "content_types": ["anime"],
  "genres": ["action", "drama"],
  "moods": ["intense"],
  "preferred_style": "mainstream",
  "custom_prompt": ""
}
```

### Response from Backend
```json
{
  "user_id": "user-123",
  "session_id": "uuid-123",
  "count": 4,
  "recommendations": [
    {
      "recommendation_id": "uuid-123_0",
      "content_id": "anime_001",
      "title": "Attack on Titan",
      "content_type": "anime",
      "genres": ["action", "drama", "fantasy"],
      "mood": ["intense", "dark", "thrilling"],
      "rating": 9.0,
      "description": "Humanity fights for survival...",
      "explanation": "AI analysis here...",
      "rank": 1,
      
      "mal_score": 9.09,              ✨ REAL from MAL
      "imdb_score": null,             (not applicable for anime)
      "cover_image": "https://...",   ✨ REAL from MAL CDN
      "external_metadata": {          ✨ REAL metadata
        "description": "Humanity...",
        "genres": ["Action", "Drama", "Fantasy"],
        "year": 2013,
        "rating_count": 2000000
      }
    },
    ... more recommendations ...
  ]
}
```

---

## 🔐 Error Handling Flow

```
API Call Attempt
    │
    ├─ Success ✅
    │   └─ Return real data
    │       └─ Cache it
    │           └─ Display with all badges
    │
    └─ Failure ❌
        ├─ Jikan fails (MAL score)
        │   └─ mal_score = null
        │       └─ Hide blue badge
        │
        ├─ OMDb fails (IMDb score)
        │   └─ imdb_score = null
        │       └─ Hide yellow badge
        │
        ├─ Gemini fails (explanation)
        │   └─ explanation = default
        │       └─ Show generic text
        │
        └─ No crash! Keep displaying
            └─ Graceful degradation
```

---

## 📈 Performance Metrics

```
Scenario 1: First Recommendation Request
├─ API calls needed: 3-4 (Jikan + OMDb + Gemini)
├─ Data volume: ~2-3 KB per item
├─ Time: ~500-800ms
└─ Caching: NO (first time)

Scenario 2: Second Request (Same Title)
├─ API calls needed: 0 (from cache)
├─ Data volume: ~2-3 KB (memory)
├─ Time: ~5-10ms
└─ Caching: YES (instant!)

Scenario 3: Cached but Different Content Type
├─ API calls: 1-2 (new type needed)
├─ Data volume: ~2-3 KB per new item
├─ Time: ~300-500ms
└─ Caching: PARTIAL
```

---

**This is how OtakuVerse gets REAL DATA! 🎌✨**
