# 🎌 OtakuVerse

> **A Multi-Agent Entertainment Recommendation System Built with Google's Agent Development Kit**

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.0-green)](https://fastapi.tiangolo.com/)
[![Google ADK](https://img.shields.io/badge/Google%20ADK-Latest-red)](https://developers.google.com/generative-ai/api-client-library/python)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

OtakuVerse is an intelligent, multi-agent entertainment recommendation system that unifies content discovery across **9 content types**: anime, movies, web series, manga, manhwa, light novels, novels, comics, and games.

Built as a capstone project for Google's **5-Day AI Agents Intensive**, OtakuVerse demonstrates enterprise-grade multi-agent orchestration using specialized agents that work in concert to deliver personalized, context-aware recommendations.

---

## ✨ Features

### 🤖 Multi-Agent Architecture
- **Orchestrator Agent**: Manages workflow and user session context
- **Catalog Search Agent**: Searches across 9 content type catalogs
- **History Agent**: Tracks user preferences and prevents duplicate recommendations
- **Mood Mapping Agent**: Intelligently translates user emotions to content attributes
- **Ranking Agent**: Orders recommendations by relevance with natural language explanations
- **Enrichment Agent**: Fetches real ratings from MyAnimeList and IMDb

### 🎯 Smart Recommendation Engine
- **Multi-Modal Search**: Simultaneously query across all content types
- **Mood-Based Filtering**: 8 user mood categories (HAPPY, SAD, EXCITED, CALM, MELANCHOLIC, ADVENTUROUS, NOSTALGIC, INTROSPECTIVE)
- **Genre-Aware**: Multiple genre tags per item for precise filtering
- **History Tracking**: SQLite database prevents recommending already-consumed content
- **AI Explanations**: Every recommendation includes reasoning for why it matches user preferences

### 🔌 REST API Backend
- FastAPI server with CORS support
- `/recommendations` - Get personalized recommendations
- `/search` - Search across all catalogs
- `/catalog/{type}` - Browse content by type
- `/history` - Manage user watch history
- `/health` - Health check endpoint

### 🎨 React Frontend
- Real-time recommendation display
- Advanced filtering (mood, genre, content type)
- Search functionality with autocomplete
- Watch history tracking
- User profile and preferences
- Responsive design with Tailwind CSS

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- Node.js 16+ (for frontend)
- Git

### Backend Setup

1. **Clone the repository**
```bash
git clone https://github.com/Ironomism1/Otakuverse.git
cd Otakuverse
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Start backend server**
```bash
python -m uvicorn api.server:app --host 127.0.0.1 --port 8001
```

Backend will be available at `http://127.0.0.1:8001`

### Frontend Setup

1. **Navigate to frontend directory**
```bash
cd Frontend
```

2. **Install dependencies**
```bash
npm install
```

3. **Start development server**
```bash
npm run dev
```

Frontend will be available at `http://localhost:3001`

---

## 📁 Project Structure

```
OtakuVerse/
├── api/
│   ├── __init__.py
│   └── server.py              # FastAPI application with endpoints
│
├── catalog_agent/
│   ├── __init__.py
│   ├── agent.py               # Catalog search and recommendation logic
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
│
├── history_agent/
│   ├── __init__.py
│   ├── agent.py               # User history management
│   └── db.py                  # SQLite database interface
│
├── mood_agent/
│   ├── __init__.py
│   └── agent.py               # Mood extraction and mapping
│
├── ranking_agent/
│   ├── __init__.py
│   └── agent.py               # Ranking and explanation generation
│
├── orchestrator/
│   ├── __init__.py
│   └── agent.py               # Main orchestrator agent
│
├── Frontend/
│   ├── src/
│   ├── components/
│   ├── pages/
│   ├── services/
│   ├── package.json
│   ├── vite.config.ts
│   └── tsconfig.json
│
├── requirements.txt           # Python dependencies
├── .env.example               # Environment variable template
├── README.md                  # Project documentation
└── OtakuVerse_Writeup.docx    # Capstone project writeup
```

---

## 🔧 Core Technologies

### Backend
- **Framework**: Google Agent Development Kit (ADK)
- **API**: FastAPI + Uvicorn
- **Database**: SQLite3
- **Data Format**: JSON catalogs
- **AI Model**: Gemini 2.5-Flash
- **External APIs**: Jikan (anime), OMDb (movies/series)

### Frontend
- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **HTTP Client**: Axios
- **State Management**: Zustand

---

## 📊 Architecture Overview

```
┌─────────────────────────────────────────────┐
│         React Frontend (localhost:3001)     │
│  - Preference Collection                    │
│  - Real-time Recommendation Display         │
│  - Search & Filtering UI                    │
└────────────────┬────────────────────────────┘
                 │ HTTP REST API
                 ↓
┌─────────────────────────────────────────────┐
│    FastAPI Backend (127.0.0.1:8001)         │
│  - Request Validation & Routing             │
│  - Database Persistence                     │
│  - Multi-Agent Orchestration                │
└────────────────┬────────────────────────────┘
     ┌───────────┼───────────┐
     ↓           ↓           ↓
┌─────────┐ ┌─────────┐ ┌─────────┐
│ Gemini  │ │ Catalog │ │External │
│ Agent   │ │ Agent   │ │  APIs   │
└─────────┘ └─────────┘ └─────────┘
```

---

## 🎯 How It Works

### Recommendation Flow

1. **User Input**: User selects mood, genres, and content types via frontend
2. **API Request**: Frontend sends POST request to `/recommendations` endpoint
3. **Mood Translation**: Backend maps user mood enum to content mood attributes
   - `HAPPY` → `fun`, `wholesome`, `heartwarming`, `inspiring`
   - `EXCITED` → `thrilling`, `epic`, `intense`, `cool`
   - And 6 more mood translations...
4. **Catalog Search**: Agents query JSON catalogs by genre, mood, content type
5. **History Filtering**: System removes already-consumed content from results
6. **Ranking**: Recommendations ranked by relevance and quality
7. **Explanation**: AI generates natural language explanation for each item
8. **Response**: Frontend displays recommendations with metadata and ratings

### Example Request/Response

**Request:**
```json
{
  "user_id": "user_123",
  "moods": ["happy"],
  "genres": ["action", "adventure"],
  "content_types": ["anime"],
  "limit": 10
}
```

**Response:**
```json
{
  "user_id": "user_123",
  "session_id": "session_abc123",
  "criteria": {
    "moods": ["happy"],
    "genres": ["action", "adventure"],
    "content_types": ["anime"]
  },
  "count": 3,
  "recommendations": [
    {
      "recommendation_id": "session_abc123_0",
      "title": "Attack on Titan",
      "content_type": "anime",
      "genres": ["action", "dark", "dramatic"],
      "mood": ["intense", "thrilling"],
      "rating": 8.5,
      "explanation": "This action-packed anime matches your preference for intense, thrilling content with high production value.",
      "rank": 1
    },
    // ... more recommendations
  ]
}
```

---

## 🌟 Key Features Explained

### Mood Mapping Intelligence
The system intelligently maps 8 user-facing emotions to 16+ content mood attributes:
- **User Moods**: HAPPY, SAD, EXCITED, CALM, MELANCHOLIC, ADVENTUROUS, NOSTALGIC, INTROSPECTIVE
- **Content Moods**: intense, thrilling, dramatic, romantic, emotional, epic, suspenseful, beautiful, mind-bending, cool, fun, wholesome, heartwarming, inspiring, dark, thoughtful

### Multi-Type Content Support
Unified search across 9 different content categories:
- 📺 **Anime** - Japanese animation
- 🎬 **Movies** - Cinema films
- 📹 **Web Series** - Online streaming content
- 📖 **Manga** - Japanese comics
- 🌐 **Manhwa** - Korean comics
- 📚 **Light Novels** - Japanese light fiction
- 📕 **Novels** - Traditional novels
- 💭 **Comics** - Western comics
- 🎮 **Games** - Video games

### History-Aware Filtering
Prevents recommending previously consumed content:
- SQLite database tracks user watch history
- Automatically filters results before returning recommendations
- Maintains viewing preferences and ratings

---

## 🔐 Environment Variables

Create a `.env` file based on `.env.example`:

```env
# API Configuration
API_HOST=127.0.0.1
API_PORT=8001
API_DEBUG=False

# Database
DATABASE_PATH=./otakuverse.db

# Gemini API
GOOGLE_API_KEY=your_google_api_key_here

# Frontend
VITE_API_URL=http://127.0.0.1:8001
```

---

## 📖 API Endpoints

### Recommendations
```bash
POST /recommendations
Content-Type: application/json

{
  "user_id": "string",
  "genres": ["string"],
  "moods": ["string"],
  "content_types": ["string"],
  "limit": 10
}
```

### Search
```bash
GET /search?q=query&limit=25
```

### Catalog
```bash
GET /catalog/{content_type}
GET /catalog/all
```

### History
```bash
GET /users/{user_id}/history
POST /users/{user_id}/history
GET /users/{user_id}/history?content_type=anime
```

### Health Check
```bash
GET /health
```

---

## 🎓 Course Connection

This project is built as a capstone submission for Google's **5-Day AI Agents Intensive** course, demonstrating:

- **Day 1**: Multi-agent architecture and specialized agent design
- **Day 2**: Custom tools system for agent collaboration
- **Day 3**: Session and persistent memory management
- **Day 4**: Observability and recommendation quality evaluation
- **Day 5**: Production-ready deployment patterns

---

## 📊 Database Schema

### Users Table
```sql
CREATE TABLE users (
    user_id TEXT PRIMARY KEY,
    preferences JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### History Table
```sql
CREATE TABLE content_history (
    id INTEGER PRIMARY KEY,
    user_id TEXT,
    content_id TEXT,
    content_type TEXT,
    title TEXT,
    rating FLOAT,
    watched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
```

### Recommendations Table
```sql
CREATE TABLE recommendations (
    id INTEGER PRIMARY KEY,
    user_id TEXT,
    session_id TEXT,
    content_id TEXT,
    explanation TEXT,
    rank INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
```

---

## 🧪 Testing

### Run Backend Tests
```bash
pytest tests/
```

### Test Specific Endpoint
```bash
curl -X POST http://127.0.0.1:8001/recommendations \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test_user",
    "moods": ["happy"],
    "genres": ["action"],
    "content_types": ["anime"]
  }'
```

---

## 🐛 Troubleshooting

### Backend won't start
- Check if port 8001 is in use: `lsof -i :8001`
- Kill existing process: `kill -9 <PID>`
- Verify Python 3.10+: `python --version`

### Frontend connection errors
- Ensure backend is running on `127.0.0.1:8001`
- Check `.env` file has correct `VITE_API_URL`
- Clear browser cache and refresh

### No recommendations returned
- Check user mood value matches mapping (case-sensitive)
- Verify content_types are valid (anime, movies, etc.)
- Check catalog JSON files have data

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Shriyansh Mishra**
- GitHub: [@Ironomism1](https://github.com/Ironomism1)
- Project: 5-Day AI Agents Intensive Capstone

---

## 🙏 Acknowledgments

- Google Agent Development Kit (ADK) team
- Kaggle and Google for the 5-Day AI Agents Intensive course
- Contributors and testers

---

## 📞 Support

For issues, questions, or feedback:
- Open an issue on [GitHub Issues](https://github.com/Ironomism1/Otakuverse/issues)
- Contact via GitHub profile

---

## 🎬 Getting Started Video

[Add link to demo video if available]

---

## 📚 Additional Resources

- [Google ADK Documentation](https://developers.google.com/generative-ai/api-client-library/python)
- [Gemini API Guide](https://ai.google.dev/)
- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)
- [React Documentation](https://react.dev/)

---

**Made with ❤️ for the AI Agents Intensive Community**
