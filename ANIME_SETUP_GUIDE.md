# OtakuVerse - Anime Recommendation System - Quick Start

## ✅ What I Fixed

Your OtakuVerse app has been fixed and is **NOW 100% FOCUSED ON ANIME!**

### Issues Fixed:
1. **Catalog Search Broken** - Fixed genre and mood search algorithms to properly match anime
2. **Anime Database** - Expanded anime catalog from 8 to 30 high-quality anime titles
3. **Backend API** - Simplified and optimized for anime recommendations
4. **Search Logic** - Fixed case-sensitivity and exact matching for genres/moods

### New Features:
- ✅ 30 anime titles with proper genres and moods
- ✅ Genre-based search (action, romance, comedy, etc.)
- ✅ Mood-based search (intense, funny, emotional, etc.)
- ✅ Combined genre + mood filtering
- ✅ User history tracking
- ✅ Recommendation persistence

---

## 📺 How to Use

### 1. Start the Backend Server

```bash
cd otakuverse
python -m uvicorn api.server:app --host 127.0.0.1 --port 8001 --reload
```

### 2. Start the Frontend

```bash
cd otakuverse/Frontend
npm install
npm run dev
```

### 3. Navigate to the App
Open `http://localhost:5173` in your browser

---

## 🎬 Available Anime

### Top 30 Anime in System:

**Action/Intense:**
- Attack on Titan (9.0/10)
- Fullmetal Alchemist: Brotherhood (9.1/10)
- Demon Slayer (8.7/10)
- Jujutsu Kaisen (8.6/10)
- Vinland Saga (8.9/10)

**Thriller/Psychological:**
- Death Note (8.8/10)
- Steins;Gate (9.0/10)
- Monster (8.8/10)
- Erased (8.5/10)

**Romance/Emotional:**
- Your Name (8.4/10)
- A Silent Voice (8.9/10)
- Fruits Basket (8.5/10)

**Comedy/Fun:**
- One Punch Man (8.4/10)
- Mob Psycho 100 (8.8/10)
- Spy x Family (8.7/10)
- Cowboy Bebop (8.9/10)

**Adventure:**
- One Piece (8.3/10)
- Naruto (8.1/10)
- My Hero Academia (8.2/10)

**Sci-Fi/Dark:**
- Neon Genesis Evangelion (8.6/10)
- Ergo Proxy (8.1/10)
- Tokyo Ghoul (8.0/10)
- Parasyte (8.2/10)

**Fantasy:**
- That Time I Got Reincarnated as a Slime (7.8/10)
- Re:Zero (8.4/10)
- Code Geass (8.5/10)

**Thriller/Mystery:**
- The Promised Neverland (8.4/10)
- Great Teacher Onizuka (8.2/10)
- Puella Magi Madoka Magica (8.3/10)

---

## 🔍 How Search Works

### Search by Mood + Genre:
```
Request:
- Content Type: "anime"
- Mood: ["intense"]
- Genres: ["action"]

Results:
- Attack on Titan
- Demon Slayer
- Vinland Saga
- Jujutsu Kaisen
```

### Search by Genre Only:
```
Request:
- Content Type: "anime"
- Genres: ["romance"]

Results:
- Your Name
- A Silent Voice
- Fruits Basket
```

### Search by Mood Only:
```
Request:
- Content Type: "anime"
- Moods: ["funny"]

Results:
- One Punch Man
- Mob Psycho 100
- Spy x Family
```

---

## 🐛 Testing Locally

Run the test script to verify everything works:

```bash
python test_anime_recommendations.py
```

This will test:
- ✓ Catalog loading (30 anime)
- ✓ Genre search
- ✓ Mood search
- ✓ Combined searches
- ✓ Content filtering

---

## 📝 API Endpoints

### Get Anime Recommendations
```bash
POST /recommendations
{
  "user_id": "user123",
  "genres": ["action"],
  "moods": ["intense"],
  "content_types": ["anime"]
}
```

### Get All Anime Catalog
```bash
GET /catalog/anime
```

### Add to Watch History
```bash
POST /users/{user_id}/history
{
  "content_id": "anime_001",
  "content_type": "anime",
  "title": "Attack on Titan",
  "rating": 9.0
}
```

### Get User History
```bash
GET /users/{user_id}/history
```

---

## 🎯 Genres Supported

action, adventure, comedy, drama, fantasy, horror, romance, sci-fi, supernatural, psychological, thriller, slice of life, sports, mecha, isekai, cyberpunk, steampunk, school, family, historical, dark, mystery, noir

---

## 😊 Moods Supported

intense, thrilling, dramatic, funny, fun, wholesome, romantic, emotional, beautiful, inspiring, epic, cool, mind-bending, suspenseful, heartwarming, dark, thoughtful, strategic

---

## ✨ Example Usage

1. **User wants action anime:**
   - Select "Anime" content type
   - Set mood to "intense"
   - Add genre "action"
   - Get recommendations like Attack on Titan, Demon Slayer, etc.

2. **User wants comedy anime:**
   - Select "Anime" content type
   - Set mood to "fun"
   - Add genre "comedy"
   - Get recommendations like One Punch Man, Mob Psycho 100, etc.

3. **User wants romance anime:**
   - Select "Anime" content type
   - Set mood to "emotional"
   - Add genre "romance"
   - Get recommendations like Your Name, A Silent Voice, etc.

---

## 📊 What Changed

| Before | After |
|--------|-------|
| 8 anime titles | 30 anime titles |
| Broken genre search | Working genre search |
| Broken mood search | Working mood search |
| Movies, comics mixed in | **ANIME ONLY FOCUS** |
| No search logic | Proper genre/mood matching |

---

## 🚀 System Ready!

Your anime recommendation system is now **fully functional and tested**!

Just select:
1. Anime as content type
2. Your mood
3. Your preferred genres
4. Get perfect anime recommendations!

Happy watching! 🎌

