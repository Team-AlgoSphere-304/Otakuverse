import React, { useState, useEffect } from 'react';
import './AnimeSearch.css';
import LoadingScreen from './LoadingScreen';
import { useAuthStore } from '../store/useStore';
import { Heart, Bookmark, History as HistoryIcon } from 'lucide-react';

interface AnimeItem {
  content_id: string;
  title: string;
  genres: string[];
  mal_score: number;
  description: string;
  cover_image: string;
  episodes?: number;
  status?: string;
  content_type?: string;
}

interface SearchResult {
  query: string;
  results: AnimeItem[];
  from_cache: boolean;
  count: number;
}

export default function AnimeSearch() {
  const [searchQuery, setSearchQuery] = useState('');
  const [results, setResults] = useState<AnimeItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [searched, setSearched] = useState(false);
  const [selectedItem, setSelectedItem] = useState<AnimeItem | null>(null);
  const [watchList, setWatchList] = useState<Set<string>>(new Set());
  const { user } = useAuthStore();

  // Load watchlist from localStorage
  useEffect(() => {
    if (user?.id) {
      const saved = localStorage.getItem(`watchlist_${user.id}`);
      if (saved) {
        try {
          const items = JSON.parse(saved);
          setWatchList(new Set(items.map((item: any) => item.content_id)));
        } catch (error) {
          console.error('Failed to load watchlist:', error);
        }
      }
    }
  }, [user?.id]);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (searchQuery.trim().length < 2) {
      alert('Please enter at least 2 characters');
      return;
    }

    setLoading(true);
    setSearched(true);

    try {
      // Log to search history
      if (user?.id) {
        const historyKey = `search_history_${user.id}`;
        const existing = localStorage.getItem(historyKey);
        const history = existing ? JSON.parse(existing) : [];
        
        // Remove if already exists and add to top
        const filtered = history.filter((item: any) => item.query !== searchQuery);
        filtered.unshift({
          query: searchQuery,
          timestamp: new Date().toISOString(),
          count: 0 // Will update after search
        });
        
        // Keep only last 20 searches
        if (filtered.length > 20) filtered.pop();
        localStorage.setItem(historyKey, JSON.stringify(filtered));
      }

      const response = await fetch(
        `http://127.0.0.1:8001/search?q=${encodeURIComponent(searchQuery)}&limit=25`
      );

      if (!response.ok) {
        throw new Error(`Search failed: ${response.statusText}`);
      }

      const data: SearchResult = await response.json();
      setResults(data.results);
      
      // Update search history with result count
      if (user?.id) {
        const historyKey = `search_history_${user.id}`;
        const history = JSON.parse(localStorage.getItem(historyKey) || '[]');
        if (history.length > 0) {
          history[0].count = data.results.length;
          localStorage.setItem(historyKey, JSON.stringify(history));
        }
      }
    } catch (error) {
      console.error('Search error:', error);
      alert('Search failed. Please try again.');
      setResults([]);
    } finally {
      setLoading(false);
    }
  };

  const handleClearSearch = () => {
    setSearchQuery('');
    setResults([]);
    setSearched(false);
    setSelectedItem(null);
  };

  const addToWatchList = (item: AnimeItem) => {
    if (!user?.id) {
      alert('Please login to add to watch list');
      return;
    }

    const watchlistKey = `watchlist_${user.id}`;
    const existing = localStorage.getItem(watchlistKey);
    let watchlistItems = existing ? JSON.parse(existing) : [];

    // Check if already exists
    const exists = watchlistItems.some((w: any) => w.content_id === item.content_id);
    if (!exists) {
      watchlistItems.push({
        ...item,
        added_at: new Date().toISOString()
      });
      localStorage.setItem(watchlistKey, JSON.stringify(watchlistItems));
      setWatchList(new Set([...watchList, item.content_id]));
    }
  };

  const removeFromWatchList = (contentId: string) => {
    if (!user?.id) return;

    const watchlistKey = `watchlist_${user.id}`;
    const existing = localStorage.getItem(watchlistKey);
    if (existing) {
      let watchlistItems = JSON.parse(existing);
      watchlistItems = watchlistItems.filter((w: any) => w.content_id !== contentId);
      localStorage.setItem(watchlistKey, JSON.stringify(watchlistItems));
      const newSet = new Set(watchList);
      newSet.delete(contentId);
      setWatchList(newSet);
    }
  };

  return (
    <div className="anime-search-container">
      <div className="search-header">
        <h1>🔍 Search Anime</h1>
        <p>Find anime, manga, movies, and TV shows</p>
      </div>

      {/* Search Form */}
      <form onSubmit={handleSearch} className="search-form">
        <div className="search-input-group">
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search anything (e.g., 'Naruto', 'One Piece', 'Death Note')..."
            className="search-input"
            disabled={loading}
          />
          <button type="submit" className="search-button" disabled={loading}>
            {loading ? '⏳ Searching...' : '🔍 Search'}
          </button>
          {searched && (
            <button type="button" onClick={handleClearSearch} className="clear-button">
              ✕ Clear
            </button>
          )}
        </div>
      </form>

      {loading && <LoadingScreen />}

      {/* Search Results */}
      {searched && results.length > 0 && (
        <div className="search-results">
          <h2>Search Results for "{searchQuery}" ({results.length} found)</h2>
          <div className="anime-grid">
            {results.map((item) => (
              <div
                key={item.content_id}
                className="anime-card"
                onClick={() => setSelectedItem(item)}
              >
                <img
                  src={item.cover_image}
                  alt={item.title}
                  className="anime-cover"
                  onError={(e) => {
                    (e.target as HTMLImageElement).src =
                      'https://via.placeholder.com/200x300?text=No+Image';
                  }}
                />
                <div className="anime-info">
                  <h3>{item.title}</h3>
                  <div className="rating">⭐ {item.mal_score.toFixed(1)}</div>
                  {item.genres && (
                    <div className="genres">
                      {item.genres.slice(0, 2).map((g) => (
                        <span key={g} className="genre-tag">
                          {g}
                        </span>
                      ))}
                    </div>
                  )}
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      if (watchList.has(item.content_id)) {
                        removeFromWatchList(item.content_id);
                      } else {
                        addToWatchList(item);
                      }
                    }}
                    className={`watchlist-button ${watchList.has(item.content_id) ? 'active' : ''}`}
                  >
                    {watchList.has(item.content_id) ? '✓ Added' : '+ Watch List'}
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* No Results Message */}
      {searched && results.length === 0 && !loading && (
        <div className="no-results">
          <p>❌ No anime found for "{searchQuery}"</p>
          <p>Try searching with different keywords</p>
        </div>
      )}

      {/* Empty State */}
      {!searched && !loading && (
        <div className="empty-catalog">
          <p>🔍 Start searching for anime, manga, movies, or TV shows!</p>
        </div>
      )}

      {/* Detail Modal */}
      {selectedItem && (
        <div className="modal-overlay" onClick={() => setSelectedItem(null)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <button className="close-button" onClick={() => setSelectedItem(null)}>
              ✕
            </button>
            <div className="modal-body">
              <img
                src={selectedItem.cover_image}
                alt={selectedItem.title}
                className="modal-cover"
              />
              <div className="modal-info">
                <h2>{selectedItem.title}</h2>
                <div className="modal-rating">MAL Rating: ⭐ {selectedItem.mal_score.toFixed(1)}/10</div>
                {selectedItem.episodes && (
                  <p className="modal-detail">Episodes: {selectedItem.episodes}</p>
                )}
                {selectedItem.status && (
                  <p className="modal-detail">Status: {selectedItem.status}</p>
                )}
                {selectedItem.genres && (
                  <div className="modal-genres">
                    {selectedItem.genres.map((g) => (
                      <span key={g} className="genre-badge">
                        {g}
                      </span>
                    ))}
                  </div>
                )}
                <div className="modal-description">
                  <h3>Synopsis</h3>
                  <p>{selectedItem.description || 'No description available'}</p>
                </div>
                <button
                  onClick={() => {
                    if (watchList.has(selectedItem.content_id)) {
                      removeFromWatchList(selectedItem.content_id);
                    } else {
                      addToWatchList(selectedItem);
                    }
                  }}
                  className={`watchlist-button-modal ${watchList.has(selectedItem.content_id) ? 'active' : ''}`}
                >
                  <Bookmark size={18} />
                  {watchList.has(selectedItem.content_id) ? 'Remove from Watch List' : 'Add to Watch List'}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
