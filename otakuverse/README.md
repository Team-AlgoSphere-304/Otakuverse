# 🎌 OtakuVerse - Multi-Agent Entertainment Recommendation System

A sophisticated backend system built with **Google Agent Development Kit (ADK)** and **Python** that provides personalized entertainment recommendations across a full universe of content types using multi-agent orchestration.

## 🌟 Features

- **Multi-Agent Architecture** - Orchestrated agents for different recommendation stages
- **Comprehensive Content Catalog** - 8 content types with 64+ recommendations
  - Anime, Movies, Web Series, Manga, Manhwa, Comics, Light Novels, Novels, Games
- **Smart Recommendation Engine** - Based on mood, genres, content type preferences
- **History Tracking** - SQLite database to track consumed content and avoid duplicates
- **REST API** - FastAPI endpoints for easy frontend integration
- **CLI Interface** - Interactive command-line for local testing
- **Gemini AI Integration** - Powered by Google's Gemini model

## 📋 Tech Stack

- **Language**: Python 3.10+
- **Agent Framework**: Google ADK
- **API**: FastAPI + Uvicorn
- **Database**: SQLite
- **Data Storage**: JSON catalogs
- **AI Model**: Gemini 2.5 Flash

## 🏗️ Project Structure

```
otakuverse/
├── orchestrator/
│   ├── __init__.py
│   └── agent.py              # Main orchestrator agent
├── mood_agent/
│   ├── __init__.py
│   └── agent.py              # Mood extraction agent
├── history_agent/
│   ├── __init__.py
│   ├── agent.py              # History management agent
│   └── db.py                 # SQLite database wrapper
├── catalog_agent/
│   ├── __init__.py
│   ├── agent.py              # Catalog search agent
│   └── catalogs/
│       ├── anime.json
│       ├── movies.json
│       ├── web_series.json
│       ├── manga.json
│       ├── manhwa.json
│       ├── comics.json
│       ├── light_novels.json
│       ├── novels.json
│       └── games.json
├── ranking_agent/
│   ├── __init__.py
│   └── agent.py              # Recommendation ranking agent
├── api/
│   ├── __init__.py
│   └── server.py             # FastAPI application
├── main.py                   # CLI entry point
├── requirements.txt          # Python dependencies
├── .env.example             # Example environment variables
└── README.md                # This file
```

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- Google API key with Gemini API access
- pip (Python package manager)

### Installation

1. **Clone or navigate to the project**:
```bash
cd otakuverse
```

2. **Create and activate a virtual environment** (recommended):
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

4. **Set up environment variables**:
```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your GOOGLE_API_KEY
```

## 🎮 Usage

### CLI Mode (Local Development)

Run the interactive CLI application:

```bash
python main.py
```

The CLI will guide you through:
1. Creating/logging into your account
2. Selecting content types
3. Specifying mood and genre preferences
4. Receiving personalized recommendations
5. Saving content to your history

### API Mode (for Frontend)

Start the FastAPI server:

```bash
# Option 1: Direct python
python -m uvicorn otakuverse.api.server:app --reload --host 0.0.0.0 --port 8000

# Option 2: From api directory
cd api
python -m uvicorn server:app --reload
```

The API will be available at `http://localhost:8000`

**API Documentation** (interactive):
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 📡 API Endpoints

### User Management

- **POST** `/users` - Create or update user
- **GET** `/users/{user_id}` - Get user profile

### Content History

- **GET** `/users/{user_id}/history` - Get user's consumption history
- **POST** `/users/{user_id}/history` - Add content to history

### Recommendations

- **POST** `/recommendations` - Get personalized recommendations
- **GET** `/recommendations/{user_id}` - Get past recommendations

### Content Types

- **GET** `/content-types` - Get available content types

### Health Check

- **GET** `/health` - Server health status

## 📝 API Usage Examples

### 1. Create a User
```bash
curl -X POST "http://localhost:8000/users" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user123", "preferences": {}}'
```

### 2. Get Recommendations
```bash
curl -X POST "http://localhost:8000/recommendations" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "genres": ["action", "adventure"],
    "moods": ["intense", "thrilling"],
    "content_types": ["anime", "movies", "web_series"]
  }'
```

### 3. Add to History
```bash
curl -X POST "http://localhost:8000/users/user123/history" \
  -H "Content-Type: application/json" \
  -d '{
    "content_id": "anime_001",
    "content_type": "anime",
    "title": "Attack on Titan",
    "rating": 9.0,
    "notes": "Amazing story and animation!"
  }'
```

## 🤖 Multi-Agent Architecture

### Agent Roles

1. **Orchestrator Agent**
   - Main coordinator
   - Manages conversation flow
   - Delegates to specialized agents
   - Ensures user requirements are met

2. **Mood Agent**
   - Extracts user mood and preferences
   - Processes natural language input
   - Identifies genres and styles

3. **Catalog Agent**
   - Searches across all content catalogs
   - Filters by genres, moods, content types
   - Returns relevant matches

4. **History Agent**
   - Manages user consumption history
   - Prevents duplicate recommendations
   - Tracks user preferences over time

5. **Ranking Agent**
   - Ranks recommendations by relevance
   - Provides personalized explanations
   - Optimizes recommendation order

## 📚 Available Content

Each content type has 8 sample entries. Expand the JSON catalogs to add more:

- **Anime**: Attack on Titan, Death Note, Your Name, Fullmetal Alchemist, etc.
- **Movies**: Inception, The Shawshank Redemption, Interstellar, The Dark Knight, etc.
- **Web Series**: Stranger Things, The Crown, Breaking Bad, The Mandalorian, etc.
- **Manga**: One Piece, Naruto, Death Note, Fullmetal Alchemist, etc.
- **Manhwa**: Solo Leveling, Tower of God, The God of High School, etc.
- **Comics**: The Amazing Spider-Man, The Dark Knight Returns, Watchmen, etc.
- **Light Novels**: That Time I Got Reincarnated as a Slime, Sword Art Online, etc.
- **Novels**: The Hobbit, 1984, Pride and Prejudice, Harry Potter, etc.
- **Games**: Zelda: BotW, The Witcher 3, Dark Souls, Elden Ring, etc.

## 🔧 Configuration

### Environment Variables

Create a `.env` file (copy from `.env.example`):

```env
GOOGLE_API_KEY=your_api_key_here
GEMINI_MODEL=models/gemini-2.5-flash
DATABASE_PATH=otakuverse.db
API_HOST=0.0.0.0
API_PORT=8000
```

## 📊 Database Schema

### Users Table
- `user_id` - Primary key
- `created_at` - Account creation timestamp
- `preferences` - JSON preferences storage

### Content History Table
- `id` - Primary key
- `user_id` - Foreign key
- `content_id` - ID of watched content
- `content_type` - Type of content (anime, movie, etc.)
- `consumed_at` - When content was consumed
- `rating` - User's rating (optional)

### Recommendations Table
- `id` - Primary key
- `user_id` - Foreign key
- `recommendation_batch_id` - Session ID
- `content_id` - Recommended content ID
- `ranking` - Position in ranked list
- `created_at` - Recommendation timestamp

## 🎯 Key Features Explained

### Smart Filtering
- Automatically avoids recommending content already consumed
- Considers user history when ranking recommendations
- Filters by specific content types on demand

### Mood-Based Recommendations
- Understands mood states and matches them to content
- Supports multi-mood searches for complex preferences
- Genre and mood combination searches

### User Preferences
- Stores user history and preferences
- Tracks consumption patterns
- Enables personalized recommendations

## 🚧 Future Enhancements

- Collaborative filtering recommendations
- Machine learning models for preference prediction
- Social features (user ratings, reviews)
- Content recommendations based on similar users
- Advanced analytics dashboard
- Integration with external APIs (IMDb, MyAnimeList, etc.)

## 🛠️ Development

### Adding New Content

Edit the JSON files in `otakuverse/catalog_agent/catalogs/`:

```json
{
  "id": "unique_id",
  "title": "Content Title",
  "type": "content_type",
  "genres": ["genre1", "genre2"],
  "mood": ["mood1", "mood2"],
  "rating": 8.5,
  "description": "Content description"
}
```

### Running Tests

```bash
# CLI test
python main.py

# API test
python -m pytest tests/
```

## 📝 License

This project is built as part of the 5-Day AI Agents Intensive (Google + Kaggle).

## 👨‍💻 Author

Created with ❤️ for entertainment enthusiasts and AI agents lovers.

## 🤝 Support

For issues, questions, or suggestions, please create an issue in the repository.

---

**Enjoy discovering your next favorite entertainment with OtakuVerse! 🌟**
