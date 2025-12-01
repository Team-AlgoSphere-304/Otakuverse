# 🎌 OtakuVerse Quick Start Guide

## ⚡ 30-Second Setup

### For Windows Users:
```bash
# 1. Double-click run.bat
# 2. Choose option 1 or 2 from menu
# 3. Done!
```

### For macOS/Linux Users:
```bash
# 1. Make script executable
chmod +x run.sh

# 2. Run it
./run.sh

# 3. Choose option from menu
```

---

## 🚀 Manual Setup (If run scripts don't work)

### Step 1: Install Python Packages
```bash
pip install -r requirements.txt
```

### Step 2: Setup Environment
```bash
# Copy example env file
cp .env.example .env

# Edit .env and add GOOGLE_API_KEY
# On Windows: notepad .env
# On Mac/Linux: nano .env
```

### Step 3: Run Application

**Option A - Interactive CLI:**
```bash
python main.py
```

**Option B - REST API Server:**
```bash
python run_server.py
```

---

## 📖 What Does Each Component Do?

### Multi-Agent System

```
User Input
    ↓
┌─────────────────────────────────────┐
│   ORCHESTRATOR AGENT (Main Boss)    │
│  - Manages overall flow             │
│  - Coordinates all agents           │
└─────────────────────────────────────┘
    ↓           ↓           ↓
    ↓           ↓           ↓
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│ MOOD AGENT  │ │CATALOG AGENT│ │HISTORY AGENT│
│- Extracts  │ │- Searches   │ │- Prevents   │
│ preferences│ │ catalogs    │ │ duplicates  │
└─────────────┘ └─────────────┘ └─────────────┘
    ↓
┌─────────────────────────────────────┐
│   RANKING AGENT                     │
│  - Sorts recommendations            │
│  - Adds explanations                │
└─────────────────────────────────────┘
    ↓
Personalized Recommendations
```

### Database
- Stores user history
- Tracks consumed content
- Remembers preferences
- Prevents duplicate recommendations

### Catalogs (JSON Files)
- 64+ entertainment items
- 9 content types
- Genres, moods, ratings
- Full descriptions

---

## 🎯 Use Cases

### 1. Find Anime to Watch
```
CLI: Select anime → Specify mood (intense/thrilling) → Get recommendations
API: POST /recommendations with content_types=["anime"]
```

### 2. Quick Recommendations API
```bash
curl -X POST "http://localhost:8000/recommendations" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "myuser",
    "genres": ["action"],
    "moods": ["intense"],
    "content_types": ["anime", "movies"]
  }'
```

### 3. Track What You've Watched
```bash
curl -X POST "http://localhost:8000/users/myuser/history" \
  -H "Content-Type: application/json" \
  -d '{
    "content_id": "anime_001",
    "content_type": "anime",
    "title": "Attack on Titan",
    "rating": 9.0
  }'
```

---

## 📡 API Endpoints at a Glance

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/users` | Create user |
| GET | `/users/{id}` | Get user profile |
| GET | `/users/{id}/history` | View watched items |
| POST | `/users/{id}/history` | Add watched item |
| POST | `/recommendations` | Get recommendations |
| GET | `/recommendations/{id}` | View past recommendations |
| GET | `/content-types` | List content types |
| GET | `/health` | Check server status |

**API Documentation**: http://localhost:8000/docs (when server running)

---

## 🎬 Content Available

### Anime (8 items)
- Attack on Titan, Death Note, Your Name, Fullmetal Alchemist...

### Movies (8 items)
- Inception, The Shawshank Redemption, Interstellar, The Dark Knight...

### Web Series (8 items)
- Stranger Things, The Crown, Breaking Bad, The Mandalorian...

### Manga (8 items)
- One Piece, Naruto, Death Note, Fullmetal Alchemist...

### Manhwa (8 items)
- Solo Leveling, Tower of God, The God of High School...

### Comics (8 items)
- The Amazing Spider-Man, The Dark Knight Returns, Watchmen...

### Light Novels (8 items)
- That Time I Got Reincarnated as a Slime, Sword Art Online...

### Novels (8 items)
- The Hobbit, 1984, Pride and Prejudice, Harry Potter...

### Games (8 items)
- The Legend of Zelda: BotW, The Witcher 3, Dark Souls, Elden Ring...

---

## 🔧 File Structure Reference

```
otakuverse/
├── main.py                    ← Start here for CLI
├── run_server.py              ← Start here for API
├── run.bat / run.sh           ← Easy startup scripts
├── requirements.txt           ← Python packages
├── .env.example              ← Configuration template
│
├── api/
│   └── server.py             ← FastAPI endpoints
│
├── orchestrator/
│   └── agent.py              ← Main coordinator
│
├── mood_agent/
│   └── agent.py              ← Preference extraction
│
├── catalog_agent/
│   ├── agent.py              ← Content search
│   └── catalogs/             ← JSON data files
│       ├── anime.json
│       ├── movies.json
│       ├── web_series.json
│       ├── manga.json
│       ├── manhwa.json
│       ├── comics.json
│       ├── light_novels.json
│       ├── novels.json
│       └── games.json
│
├── history_agent/
│   ├── agent.py              ← History tools
│   └── db.py                 ← SQLite management
│
├── ranking_agent/
│   └── agent.py              ← Ranking & explanations
│
└── README.md, SETUP.md       ← Full documentation
```

---

## 💡 Common Commands

### CLI Mode
```bash
python main.py
# Then follow interactive prompts
```

### API Mode
```bash
python run_server.py
# Visit http://localhost:8000/docs
```

### Test API
```bash
# Get recommendations
curl -X POST http://localhost:8000/recommendations \
  -H "Content-Type: application/json" \
  -d '{"user_id":"test","content_types":["anime"]}'

# Check health
curl http://localhost:8000/health
```

### View Database
```bash
# Database is automatically created at: ./otakuverse.db
# Use any SQLite viewer to inspect
```

---

## ❓ FAQ

**Q: Do I need the Gemini API right now?**
A: The ADK agents are set up but the CLI and API work without them for basic recommendations. The API key is used for mood/preference extraction.

**Q: Can I add more content?**
A: Yes! Edit the JSON files in `catalog_agent/catalogs/` and add more entries with the same format.

**Q: How many recommendations can I get?**
A: Each session returns up to 10 recommendations. You can request again with different preferences.

**Q: Is the database persistent?**
A: Yes! All recommendations and history are saved to `otakuverse.db` and persist between sessions.

**Q: Can I use this with a frontend?**
A: Yes! The API is fully REST-based and ready for frontend integration. CORS is enabled.

---

## 🚨 Troubleshooting

### "Module not found" error
```bash
# Make sure you installed dependencies
pip install -r requirements.txt
```

### "Port 8000 already in use"
```bash
# Edit .env and change API_PORT to something else like 8001
```

### Database locked error
```bash
# Close all instances and delete otakuverse.db
# It will recreate on next run
```

### API not responding
```bash
# Check server is running
# Check http://localhost:8000/health
# Check firewall isn't blocking port 8000
```

---

## 🎓 Learning Path

1. **Start** → Run CLI with `python main.py`
2. **Explore** → Try different moods and genres
3. **Understand** → Read the code structure
4. **Build** → Integrate with your frontend
5. **Extend** → Add more content types

---

## 📚 Documentation Files

- `README.md` - Complete project documentation
- `SETUP.md` - Detailed setup instructions
- `QUICKSTART.md` - This file!

---

## 🎉 You're Ready!

Choose your starting point:

1. **Just want to play**: `python main.py`
2. **Building a frontend**: `python run_server.py` (use API)
3. **Want to understand code**: Check `README.md` and individual agent files
4. **Ready to deploy**: Follow deployment section in SETUP.md

---

**Questions? Check README.md for comprehensive documentation!**

**Happy recommending! 🎌**
