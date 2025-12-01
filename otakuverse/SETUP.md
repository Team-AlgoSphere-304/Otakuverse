# OtakuVerse Setup & Installation Guide

## Quick Start Guide

### Step 1: Prerequisites Check
- Python 3.10+ installed
- pip available
- Google API key with Gemini API access

### Step 2: Environment Setup

1. **Navigate to project directory**:
```bash
cd path/to/ai-agents-adk/otakuverse
```

2. **Create virtual environment**:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

### Step 3: Configure Environment Variables

1. **Copy example environment file**:
```bash
# Windows
copy .env.example .env

# macOS/Linux
cp .env.example .env
```

2. **Edit .env file** and add your credentials:
```env
GOOGLE_API_KEY=your_actual_google_api_key
GEMINI_MODEL=models/gemini-2.5-flash
DATABASE_PATH=otakuverse.db
API_HOST=0.0.0.0
API_PORT=8000
API_DEBUG=True
```

### Step 4: Running the Application

#### Option A: Run CLI (Interactive Mode)
```bash
python main.py
```

The CLI will:
1. Ask you to create a new account or use existing
2. Guide you through content type selection
3. Gather mood and genre preferences
4. Display personalized recommendations
5. Allow you to save content to history

#### Option B: Run REST API Server
```bash
python run_server.py
```

Or using uvicorn directly:
```bash
python -m uvicorn api.server:app --reload --host 0.0.0.0 --port 8000
```

**Access the API**:
- Main API: `http://localhost:8000`
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Project Components

### 1. Database Module (`history_agent/db.py`)
- SQLite database management
- User profile storage
- Content history tracking
- Recommendation history
- Functions:
  - `create_user()` - Create new user
  - `add_to_history()` - Add consumed content
  - `get_consumed_ids()` - Get content IDs to avoid duplicates
  - `save_recommendation()` - Store recommendations

### 2. Catalog Agent (`catalog_agent/agent.py`)
- Content catalog management
- Search functionality:
  - By genres
  - By moods
  - By genre + mood combination
  - By content type
- Filtering consumed content
- 64+ pre-loaded recommendations across 9 content types

### 3. Mood Agent (`mood_agent/agent.py`)
- User preference extraction
- Mood recognition
- Genre identification
- Uses Gemini for natural language processing

### 4. History Agent (`history_agent/agent.py`)
- Tools for accessing user history
- Prevents duplicate recommendations
- Tracks consumption patterns

### 5. Ranking Agent (`ranking_agent/agent.py`)
- Ranks recommendations by relevance
- Provides personalized explanations
- Optimizes recommendation order

### 6. Orchestrator Agent (`orchestrator/agent.py`)
- Main coordinator
- Manages conversation flow
- Delegates to specialized agents
- Ensures proper session handling

### 7. FastAPI Server (`api/server.py`)
- REST endpoints for all functionality
- CORS enabled for frontend integration
- Automatic API documentation
- Health checks and monitoring

### 8. CLI Interface (`main.py`)
- Interactive command-line application
- User-friendly menus
- Session management
- Real-time feedback

## API Endpoints Summary

### Users
```
POST   /users                    - Create/update user
GET    /users/{user_id}          - Get user profile
```

### History
```
GET    /users/{user_id}/history  - Get consumption history
POST   /users/{user_id}/history  - Add to history
```

### Recommendations
```
POST   /recommendations          - Get recommendations
GET    /recommendations/{user_id} - Get past recommendations
```

### System
```
GET    /content-types            - List available types
GET    /health                   - Health check
```

## Content Types Available

- 📺 **Anime** - 8 recommendations (Attack on Titan, Death Note, etc.)
- 🎬 **Movies** - 8 recommendations (Inception, Dark Knight, etc.)
- 📱 **Web Series** - 8 recommendations (Stranger Things, Breaking Bad, etc.)
- 📖 **Manga** - 8 recommendations (One Piece, Naruto, etc.)
- 🇰🇷 **Manhwa** - 8 recommendations (Solo Leveling, Tower of God, etc.)
- 💥 **Comics** - 8 recommendations (Spider-Man, Watchmen, etc.)
- 📕 **Light Novels** - 8 recommendations (SAO, Re:Zero, etc.)
- 📚 **Novels** - 8 recommendations (Lord of the Rings, 1984, etc.)
- 🎮 **Games** - 8 recommendations (Elden Ring, Witcher 3, etc.)

## Example Usage

### CLI Example
```bash
$ python main.py

🎌 Welcome to OtakuVerse 🎌

Do you have an existing account? (y/n): n
Enter a new user ID: anime_lover_123

✓ New account created!

Let's find the perfect entertainment for you!

Select content types (1-9, comma-separated): 1,4,7
✓ Selected: 📺 Anime, 📖 Manga, 📕 Light Novels

What's your current mood?: intense, thrilling
Your preferred genres: action, adventure

🔍 Searching for recommendations...
✓ Found 8 recommendations!

YOUR RECOMMENDATIONS
=====================

📌 RECOMMENDATION #1
Title:    Attack on Titan
Type:     anime
Rating:   ⭐⭐⭐⭐⭐ (9.0/10)
Genres:   action, dark, supernatural
```

### API Example
```bash
# Get recommendations via curl
curl -X POST "http://localhost:8000/recommendations" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "genres": ["action", "adventure"],
    "moods": ["intense"],
    "content_types": ["anime", "movies"]
  }'
```

## Troubleshooting

### Issue: "Import not resolved" warnings
- These are IDE warnings and don't affect runtime
- Run the application normally - it will work once dependencies are installed

### Issue: "GOOGLE_API_KEY not found"
- Ensure .env file exists in the otakuverse directory
- Verify GOOGLE_API_KEY is set with actual value
- Restart the application after updating .env

### Issue: Database locked
- Close other instances of the application
- Delete otakuverse.db and restart (will recreate)

### Issue: Port 8000 already in use
- Change API_PORT in .env file
- Or kill the process using that port

## Adding More Content

To add more recommendations:

1. Edit JSON files in `catalog_agent/catalogs/`
2. Add entries with this format:
```json
{
  "id": "unique_identifier",
  "title": "Content Title",
  "type": "content_type",
  "genres": ["genre1", "genre2"],
  "mood": ["mood1", "mood2"],
  "rating": 8.5,
  "description": "Content description"
}
```

## Performance Tips

- Recommendations are cached in memory (CatalogManager)
- SQLite provides fast local queries
- JSON loads are optimized at startup
- API supports 1000s of concurrent requests

## Next Steps

1. **Install dependencies**: `pip install -r requirements.txt`
2. **Configure .env**: Copy and fill `.env.example`
3. **Run application**: Choose CLI or API mode
4. **Test integration**: Use provided examples
5. **Deploy frontend**: Connect your frontend to API endpoints

## Support & Resources

- **Documentation**: See README.md
- **API Docs**: http://localhost:8000/docs (when server running)
- **Code Structure**: Check individual agent files for implementation details

---

**Ready to start? Run `python main.py` to begin!** 🚀
