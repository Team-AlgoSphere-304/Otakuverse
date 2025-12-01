You are GitHub Copilot. Generate a complete backend app called *OtakuVerse: a multi-agent entertainment recommendation system built with **Google Agent Development Kit (ADK)* and *Python*.

The frontend will be done separately, so focus on:
- Multi-agent architecture with ADK
- Clean Python project structure
- SQLite-based history storage
- JSON-based catalogs for content data
- Optional REST API wrapper (FastAPI) that my frontend can call

The app is inspired by the 5-Day AI Agents Intensive (Google + Kaggle) and should follow best practices from that style of multi-agent orchestration.

---

## High-Level Requirements

### Core idea

Build a backend system that recommends *entertainment content across the full universe*:

- Anime
- Movies
- Web series
- Light novels
- Novels
- Manga
- Manhwa
- Comics
- Games

Each session:
- The system must *always ask which content types* the user wants from this full universe.
- It must *never assume a default* set of types.
- It uses *mood + genres + style + content types + history* to generate recommendations.
- It must *avoid recommending items the user has already consumed, by using a **SQLite database* for history.

Use *Google ADK* for the agent layer, and *Gemini* (e.g. gemini-2.5-flash) as the default model (configurable via environment variables).

---

## Tech Stack

- Language: *Python 3.10+*
- Agent framework: *google-adk*
- Config: .env with GOOGLE_API_KEY and ADK-related environment variables
- Database: *SQLite* for user history
- Data storage for catalog: JSON files
- Optional API: *FastAPI* + *uvicorn* to expose REST endpoints for frontend

Create a requirements.txt including (at minimum):

- google-adk
- python-dotenv
- fastapi
- uvicorn
- pydantic (if needed explicitly)
- sqlite3 (standard library; don’t add to requirements)

---

## Project Structure

Create this folder structure:

```text
otakuverse/
  ├── orchestrator/
  │   ├── _init_.py
  │   └── agent.py            # Orchestrator agent (root ADK agent)
  │
  ├── mood_agent/
  │   ├── _init_.py
  │   └── agent.py            # Mood & preference extraction agent
  │
  ├── history_agent/
  │   ├── _init_.py
  │   ├── agent.py            # History ADK agent exposing tools
  │   └── db.py               # SQLite wrapper functions
  │
  ├── catalog_agent/
  │   ├── _init_.py
  │   ├── agent.py            # Catalog search agent
  │   └── catalogs/
  │       ├── anime.json
  │       ├── movies.json
  │       ├── web_series.json
  │       ├── manga.json
  │       ├── manhwa.json
  │       ├── comics.json
  │       ├── games.json
  │       ├── light_novels.json
  │       └── novels.json
  │
  ├── ranking_agent/
  │   ├── _init_.py
  │   └── agent.py            # Ranking logic + explanations
  │
  ├── api/
  │   ├── _init_.py
  │   └── server.py           # FastAPI app with endpoints
  │
  ├── main.py                 # CLI / local dev entrypoint
  ├── .env.example            # Example env variables
  ├── requirements.txt
  └── README.md