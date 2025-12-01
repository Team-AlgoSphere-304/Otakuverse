# ⚡ OtakuVerse Anime - Quick Reference

## 🎬 What's Fixed
✅ **30 Anime Titles** - Expanded from 8  
✅ **Working Genre Search** - Fixed broken logic  
✅ **Working Mood Search** - Fixed broken logic  
✅ **Anime-Only Focus** - No more movies!  
✅ **User History** - Track watched anime  
✅ **Persistent DB** - Save recommendations  

---

## 🚀 Start the App

### Terminal 1 - Backend
```bash
cd otakuverse
python -m uvicorn api.server:app --host 127.0.0.1 --port 8001
```

### Terminal 2 - Frontend
```bash
cd otakuverse/Frontend
npm run dev
```

### Open Browser
```
http://localhost:5173
```

---

## 📺 Available Anime Genres
action • adventure • comedy • drama • fantasy • horror • romance • sci-fi • supernatural • psychological • thriller • dark • mysterious • mecha • isekai

---

## 😊 Available Moods
intense • thrilling • funny • fun • wholesome • romantic • emotional • beautiful • inspiring • epic • cool • mind-bending • suspenseful • heartwarming • dark • thoughtful

---

## 🎯 How to Get Recommendations

1. **Register/Login** - Create an account
2. **Go to Recommendations** - Click "Get Recommendations"
3. **Select Anime** - Choose "Anime" as content type
4. **Pick Your Mood** - e.g., "intense", "funny", "emotional"
5. **Pick Genres** - e.g., "action", "romance", "comedy"
6. **Submit** - Click "Generate Recommendations"
7. **Enjoy** - See perfect anime for your mood!

---

## 🎬 Top Anime by Genre

### Action
- Attack on Titan (9.0)
- Fullmetal Alchemist (9.1)
- Demon Slayer (8.7)

### Romance
- A Silent Voice (8.9)
- Your Name (8.4)
- Fruits Basket (8.5)

### Comedy
- Mob Psycho 100 (8.8)
- Spy x Family (8.7)
- One Punch Man (8.4)

### Thriller
- Death Note (8.8)
- Steins;Gate (9.0)
- Monster (8.8)

### Sci-Fi
- Cowboy Bebop (8.9)
- Neon Genesis Evangelion (8.6)
- Code Geass (8.5)

---

## 🧪 Test Everything

```bash
# Test catalog locally
python test_anime_recommendations.py

# Test API
python test_api_anime.py
```

---

## 📊 System Status

| Component | Status |
|-----------|--------|
| Anime Catalog | ✅ 30 titles |
| Genre Search | ✅ Working |
| Mood Search | ✅ Working |
| Backend API | ✅ Running |
| Database | ✅ SQLite |
| User Tracking | ✅ Enabled |

---

## 🎌 You're All Set!

Your app is ready. Just:
1. Start backend
2. Start frontend
3. Select ANIME
4. Pick mood + genre
5. Get recommendations!

Happy watching! 🎬

