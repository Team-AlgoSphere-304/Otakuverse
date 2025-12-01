# 🎌 OtakuVerse - Quick Start with Real Data

## ✅ All APIs Configured

Your app is ready with:
- ✅ **Google Gemini API** - For AI recommendations
- ✅ **MyAnimeList API (Jikan)** - Real anime/manga scores & images
- ✅ **OMDb API** - Real IMDb scores & images
- ✅ **All API keys in .env**

---

## 🚀 Run the App

### Terminal 1: Start Backend
```powershell
cd "c:\Users\Shriyansh Mishra\Documents\Codes\Projects\ai-agents-adk\otakuverse"
& "C:\Users\Shriyansh Mishra\.conda\envs\otakuverse\python.exe" run_server.py
```

✅ You should see:
```
╔══════════════════════════════════════════════╗
║     🎌 OtakuVerse API 🎌                     ║
║ Multi-Agent Entertainment System              ║
╚══════════════════════════════════════════════╝

Uvicorn running on http://0.0.0.0:8000
```

### Terminal 2: Start Frontend
```powershell
cd "c:\Users\Shriyansh Mishra\Documents\Codes\Projects\ai-agents-adk\otakuverse\Frontend"
npm run dev
```

✅ You should see:
```
 VITE v6.2.0  ready in 234 ms

Local: http://localhost:3001/
```

---

## 🎮 Using the App

### Step 1: Go to Frontend
Open **http://localhost:3001** in your browser

### Step 2: Get Recommendations
1. Click **"Generate Recommendations"** button
2. Select content types (anime, movies, manga, etc.)
3. Choose mood (happy, intense, romantic, etc.)
4. Select genres (action, fantasy, drama, etc.)
5. Click **"Generate Recommendations"** button

### Step 3: See Real Data
Look for:
- 🏆 **MAL Score** (blue badge) - Real MyAnimeList rating
- 🎬 **IMDb Score** (yellow badge) - Real IMDb rating
- 🖼️ **Real Image** - Official poster from MAL/IMDb
- 💬 **AI Explanation** - Click "Why?" button to see Gemini's analysis

---

## 📊 Data You'll See

### Anime Results
```
Title: Attack on Titan
MAL Score: 9.09 ⭐
Image: [Real poster from MyAnimeList]
```

### Movie Results
```
Title: Inception
IMDb Score: 8.8 ⭐
Image: [Real poster from IMDb]
```

---

## 🔧 API Details

| API | Purpose | Status | Limits |
|-----|---------|--------|--------|
| Jikan (MAL) | Anime/manga scores & images | ✅ Free | 10 req/sec |
| OMDb | Movie/TV scores & images | ✅ Free (your key) | 100 req/day |
| Gemini | AI explanations | ✅ Active | 50 req/min |

---

## 🎯 What Changed

- ❌ **Removed**: Mock random scores
- ❌ **Removed**: Placeholder images
- ✅ **Added**: Real MAL scores from MyAnimeList
- ✅ **Added**: Real IMDb scores from OMDb
- ✅ **Added**: Real poster images
- ✅ **Added**: AI-powered explanations

---

## ✨ Features Now Live

- 🤖 **AI Recommendations** - Gemini analyzes your taste
- 🎬 **Real Ratings** - From MAL, IMDb, and other sources
- 🖼️ **Real Images** - Official posters
- 💾 **Smart Caching** - Fast repeat requests
- 🔄 **Real-time Data** - Updated via APIs

---

## 📚 Explore the Code

Read the detailed guide:
```
c:\Users\Shriyansh Mishra\Documents\Codes\Projects\ai-agents-adk\REAL_DATA_INTEGRATION.md
```

---

## 🎊 You're All Set!

**Everything is configured and ready to go.** Just run both servers and enjoy real data recommendations! 🚀
