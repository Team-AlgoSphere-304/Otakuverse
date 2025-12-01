# OtakuVerse - Command Reference Guide

## Quick Commands

### Installation & Setup
```bash
# Navigate to project
cd otakuverse

# Install dependencies
pip install -r requirements.txt

# Setup environment
copy .env.example .env
# Edit .env with your GOOGLE_API_KEY

# Create virtual environment (optional)
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
```

### Running the Application

#### CLI Mode (Interactive)
```bash
python main.py
```
- User-friendly menus
- Real-time recommendations
- History tracking
- Session management

#### API Server Mode
```bash
# Option 1: Direct
python run_server.py

# Option 2: Using uvicorn
python -m uvicorn api.server:app --reload --host 0.0.0.0 --port 8000

# Option 3: Change port
python -m uvicorn api.server:app --port 8001
```

#### Easy Startup Scripts
```bash
# Windows
run.bat              # Interactive menu

# macOS/Linux
chmod +x run.sh
./run.sh             # Interactive menu

# PowerShell
.\run.ps1            # Interactive menu
```

---

## API Requests (Using cURL)

### Create User
```bash
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{"user_id": "myuser", "preferences": {}}'
```

### Get User Profile
```bash
curl http://localhost:8000/users/myuser
```

### Get Recommendations
```bash
curl -X POST http://localhost:8000/recommendations \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "myuser",
    "genres": ["action", "adventure"],
    "moods": ["intense", "thrilling"],
    "content_types": ["anime", "movies"]
  }'
```

### Add to History
```bash
curl -X POST http://localhost:8000/users/myuser/history \
  -H "Content-Type: application/json" \
  -d '{
    "content_id": "anime_001",
    "content_type": "anime",
    "title": "Attack on Titan",
    "rating": 9.0,
    "notes": "Amazing series!"
  }'
```

### Get User History
```bash
curl http://localhost:8000/users/myuser/history
```

### Get User History (By Type)
```bash
curl http://localhost:8000/users/myuser/history?content_type=anime
```

### Get Past Recommendations
```bash
curl http://localhost:8000/recommendations/myuser
```

### Get Available Content Types
```bash
curl http://localhost:8000/content-types
```

### Health Check
```bash
curl http://localhost:8000/health
```

---

## Python API Usage

### Direct Function Calls
```python
from otakuverse.history_agent.db import HistoryDatabase
from otakuverse.catalog_agent.agent import CatalogManager

# Initialize
db = HistoryDatabase()
catalog = CatalogManager()

# Create user
db.create_user("user123")

# Add to history
db.add_to_history("user123", "anime_001", "anime", "Attack on Titan", 9.0)

# Get recommendations
results = catalog.search_by_genre_and_mood(
    genres=["action"],
    moods=["intense"],
    content_types=["anime", "movies"]
)

# Filter consumed
consumed = db.get_consumed_ids("user123")
filtered = catalog.filter_out_consumed(results, consumed)
```

---

## Configuration

### Environment Variables (.env)
```env
# Required
GOOGLE_API_KEY=your_actual_key_here

# Optional
GEMINI_MODEL=models/gemini-2.5-flash
DATABASE_PATH=otakuverse.db
API_HOST=0.0.0.0
API_PORT=8000
API_DEBUG=True
```

---

## Troubleshooting Commands

### Check Python Installation
```bash
python --version
python -m pip --version
```

### Check Installed Packages
```bash
pip list
pip show fastapi
pip show google-adk
```

### Test Database
```bash
# SQLite command line
sqlite3 otakuverse.db
.tables
.schema
.quit
```

### Reset Database
```bash
# Remove database file (it will recreate)
rm otakuverse.db  # macOS/Linux
del otakuverse.db  # Windows
```

### Check Port Usage
```bash
# Windows
netstat -ano | findstr :8000

# macOS/Linux
lsof -i :8000
```

### Kill Process on Port
```bash
# Windows
taskkill /PID <PID> /F

# macOS/Linux
kill -9 <PID>
```

---

## File Management

### Add More Content
```bash
# Edit catalog files
nano catalog_agent/catalogs/anime.json
# or
vim catalog_agent/catalogs/anime.json

# Add new entry:
{
  "id": "anime_009",
  "title": "New Anime Title",
  "type": "anime",
  "genres": ["action", "adventure"],
  "mood": ["intense", "epic"],
  "rating": 8.5,
  "description": "Description of the anime"
}
```

### View Project Structure
```bash
# List all Python files
find . -name "*.py" -type f

# List all JSON catalogs
ls catalog_agent/catalogs/

# Count total files
find . -type f | wc -l
```

---

## Development Commands

### Run with Hot Reload
```bash
python -m uvicorn api.server:app --reload
```

### Debug Mode
```bash
# Set debug in .env
API_DEBUG=True

# Run server
python run_server.py
```

### Check Syntax
```bash
# Python syntax check
python -m py_compile main.py
python -m py_compile api/server.py

# Check all Python files
python -m compileall .
```

---

## Documentation Access

### Online Documentation
```
API Docs:       http://localhost:8000/docs
Alternative:    http://localhost:8000/redoc
Health Check:   http://localhost:8000/health
```

### Local Files
```
README.md           - Complete documentation
SETUP.md            - Setup instructions
QUICKSTART.md       - Quick learning
IMPLEMENTATION.md   - Technical details
```

---

## Git Commands (if using version control)

```bash
git init
git add .
git commit -m "Initial OtakuVerse setup"
git branch
git log
```

---

## Package Management

### Update Dependencies
```bash
pip install --upgrade -r requirements.txt
```

### Generate Requirements
```bash
pip freeze > requirements.txt
```

### Virtual Environment
```bash
# Create
python -m venv venv

# Activate Windows
venv\Scripts\activate

# Activate macOS/Linux
source venv/bin/activate

# Deactivate
deactivate
```

---

## Common Issues & Solutions

### ImportError: No module named 'google.adk'
```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

### Port 8000 already in use
```bash
# Solution: Use different port
API_PORT=8001 python run_server.py
```

### Database locked
```bash
# Solution: Delete and recreate
rm otakuverse.db
python main.py  # Will recreate
```

### .env file not found
```bash
# Solution: Copy from example
cp .env.example .env
```

---

## Performance Tips

- Run API in production mode (no reload)
- Use environment variables instead of hardcoding
- Cache catalog data in memory (done automatically)
- Use connection pooling for database
- Monitor API response times

---

## Deployment Checklist

- [ ] Python 3.10+ installed
- [ ] All dependencies installed
- [ ] .env configured with API keys
- [ ] Database initialized
- [ ] API responds at /health
- [ ] Documentation accessible at /docs
- [ ] CORS configured for frontend
- [ ] Error handling tested
- [ ] Sample requests successful
- [ ] Performance acceptable

---

## Contact & Support

For detailed documentation, see:
- README.md (full guide)
- SETUP.md (installation)
- QUICKSTART.md (quick start)
- Individual file comments (code)

---

**Last Updated**: December 2024
**Version**: 1.0.0
**Status**: Production Ready
