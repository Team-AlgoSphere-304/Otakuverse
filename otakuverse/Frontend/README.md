# OtakuVerse Frontend - Complete Integration Guide

## 🎬 Overview

This is a fully integrated React + TypeScript frontend for OtakuVerse that seamlessly connects with the Python backend. It features:

- ✅ Real image loading from IMDb and MyAnimeList
- ✅ Live ratings from external sources (IMDb, MAL)
- ✅ Gemini AI-powered explanations
- ✅ Full backend API integration
- ✅ User authentication & history
- ✅ Beautiful Dark Anime-inspired UI

## 🚀 Quick Setup

### 1. Install Dependencies

```bash
npm install
```

### 2. Configure Environment Variables

Create or update `.env.local`:

```env
VITE_API_URL=http://localhost:8000/api
VITE_GEMINI_API_KEY=your_gemini_api_key_here
VITE_OMDB_API_KEY=your_omdb_api_key_here
```

**Get API Keys:**
- **Gemini API**: [Google AI Studio](https://aistudio.google.com)
- **OMDb API**: [OMDb - Free Tier Available](https://www.omdbapi.com/apikey.aspx)

### 3. Start Backend

```bash
cd ..
python run_server.py
```

### 4. Start Frontend (in new terminal)

```bash
npm run dev
```

The app will be available at `http://localhost:5173`

## 📋 Features Implemented

### ✨ Image Loading Integration
- **MyAnimeList (Jikan API)**: Fetches real posters for anime, manga, light novels
- **IMDb (OMDb API)**: Fetches real movie/series posters
- **Caching**: Images cached after first load for performance
- **Fallback**: Placeholder images if source unavailable

### ✨ Real Ratings Display
- **MyAnimeList Ratings**: For anime/manga content
- **IMDb Ratings**: For movies/series
- **Rating Counts**: User count for each rating
- **Live Updates**: Fetched on demand, not mocked

### ✨ Gemini AI Integration
- **Real Explanations**: Why each item was recommended
- **Personalized**: Based on user mood, genres, preferences
- **Natural Language**: Human-friendly recommendations

### ✨ Content Selection
- Multi-select from 9 content types
- Never pre-selected
- Visual emojis
- Selection counter

## 📁 Project Structure

```
Frontend/
├── services/
│   ├── api.ts                    # Enhanced backend API client
│   ├── geminiService.ts          # Gemini real data extraction
│   └── imageRatingService.ts     # IMDb/MAL image & rating fetching
├── components/
│   ├── RecommendationCard.tsx    # Enhanced card with real data
│   ├── PreferenceForm.tsx        # Preferences UI
│   ├── ContentTypeSelector.tsx   # Content type selection
│   └── Navbar.tsx                # Navigation
├── pages/
│   ├── Recommendations.tsx       # Main flow
│   ├── History.tsx               # User history
│   ├── Catalog.tsx               # Browse content
│   ├── Profile.tsx               # User profile
│   ├── Home.tsx                  # Landing
│   ├── Login.tsx                 # Auth
│   └── Register.tsx              # Signup
├── store/
│   └── useStore.ts               # Enhanced Zustand store
├── types.ts                      # Interfaces
└── constants.ts                  # Constants
```

## 🌐 External APIs

### MyAnimeList (Jikan API) - FREE ✅
- No API key required
- Real anime/manga data
- Images, ratings, descriptions
- Rate limit: Generous for public use

### IMDb (OMDb) - FREE TIER ✅
- Free API key (1000 requests/day)
- Movie/series posters and ratings
- [Get free key](https://www.omdbapi.com/apikey.aspx)

### Google Gemini - FREE TIER ✅
- Real AI explanations
- [Get free API key](https://aistudio.google.com)

## 🔧 Technical Details

### Image Loading Flow
1. Component receives title and content type
2. Determines source (MAL for anime, IMDb for movies)
3. Fetches in parallel with other data
4. Caches result
5. Displays with loading state

### Rating Fetching Flow
1. Component requests ratings
2. Service queries both MAL and IMDb (if applicable)
3. Caches by title + type
4. Returns structured rating data
5. UI displays source badges

### Gemini Explanation Flow
1. User views recommendation card
2. Backend passes to Gemini API
3. AI generates personalized explanation
4. Explanation displayed on card flip
5. Cached for subsequent views

## 🎯 Troubleshooting

### Images Not Loading
```
❌ Check: VITE_OMDB_API_KEY in .env.local
❌ Check: Backend running on http://localhost:8000
❌ Check: Browser console for CORS errors
✅ MAL (anime) should work without OMDb key
```

### Ratings Not Showing
```
❌ Check: VITE_GEMINI_API_KEY in .env.local
❌ Check: Network tab in DevTools
✅ MAL ratings always work (no key needed)
✅ IMDb requires key
```

### Backend Connection Failed
```
✅ Run: python run_server.py
✅ Check: http://localhost:8000/docs accessible
✅ Verify: VITE_API_URL in .env.local
✅ Check: CORS enabled (should be by default)
```

## 📊 Data Flow Diagram

```
User Input (Mood, Genres, Types)
         ↓
Backend API (recommendations)
         ↓
Frontend receives items
         ↓
Parallel fetching:
  ├─→ MyAnimeList images/ratings (anime/manga)
  ├─→ IMDb images/ratings (movies/series)
  └─→ Gemini explanations
         ↓
UI renders with real data
```

## 🚀 Production Deployment

### Build
```bash
npm run build
```

### Environment Variables for Production
```
VITE_API_URL=https://your-backend.com/api
VITE_GEMINI_API_KEY=your_production_key
VITE_OMDB_API_KEY=your_production_key
```

### Deploy to Vercel
```bash
vercel
```

### Deploy to Netlify
```bash
netlify deploy --prod --dir=dist
```

## 📚 Code Examples

### Using Image Service
```typescript
import imageRatingService from '../services/imageRatingService';

// Get MAL images for anime
const images = await imageRatingService.getMalImages('Demon Slayer', 'anime');

// Get IMDb images for movies
const images2 = await imageRatingService.getImdbImages('Inception');

// Get ratings
const ratings = await imageRatingService.getRatings('Attack on Titan', 'anime');
```

### Using Gemini Service
```typescript
import geminiService from '../services/geminiService';

// Generate explanation
const explanation = await geminiService.generateRecommendationExplanation(
  'Death Note',
  'anime',
  'introspective',
  ['thriller', 'psychological'],
  'dark and intelligent'
);
```

### Backend API Integration
```typescript
import api from '../services/api';

// Get recommendations with backend
const recs = await api.getRecommendations(
  userId,
  'happy',
  ['action', 'adventure'],
  ['anime', 'manga'],
  'dark'
);

// Get enriched item data
const enriched = await api.getEnrichedContent('Demon Slayer', 'anime');
```

## 🎨 UI Features

- Dark anime-inspired theme
- Gradient accents (purple to pink)
- Loading skeletons
- Smooth animations
- Card flip for more info
- Star rating system
- Bookmark functionality
- Responsive grid layout

## ✅ Verified Features

- ✅ Images from MyAnimeList
- ✅ Images from IMDb
- ✅ MAL Ratings display
- ✅ IMDb Ratings display
- ✅ Gemini explanations
- ✅ Backend API integration
- ✅ User authentication
- ✅ History tracking
- ✅ Real-time ratings
- ✅ Responsive design

## 🔐 Security

- API keys in `.env.local` (not committed)
- Backend validates all requests
- CORS properly configured
- No sensitive data in frontend

---

**Ready to use!** Set up `.env.local` and start the backend to begin getting AI-powered recommendations with real data.
