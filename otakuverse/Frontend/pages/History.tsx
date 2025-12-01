import React, { useState, useEffect } from 'react';
import { useAuthStore } from '../store/useStore';
import { Trash2, Search as SearchIcon, Calendar } from 'lucide-react';

interface SearchHistory {
  query: string;
  timestamp: string;
  count: number;
}

interface ViewHistory {
  title: string;
  content_type: string;
  timestamp: string;
}

const History: React.FC = () => {
  const [searchHistory, setSearchHistory] = useState<SearchHistory[]>([]);
  const [viewHistory, setViewHistory] = useState<ViewHistory[]>([]);
  const [activeTab, setActiveTab] = useState<'search' | 'views'>('search');
  const [loading, setLoading] = useState(false);
  const { user } = useAuthStore();

  useEffect(() => {
    loadHistory();
  }, [user?.id]);

  const loadHistory = async () => {
    if (!user?.id) return;
    setLoading(true);
    try {
      // Load search history
      const searchData = localStorage.getItem(`search_history_${user.id}`);
      if (searchData) {
        setSearchHistory(JSON.parse(searchData));
      }

      // Load view history
      const viewData = localStorage.getItem(`view_history_${user.id}`);
      if (viewData) {
        setViewHistory(JSON.parse(viewData));
      }
    } catch (error) {
      console.error('Failed to load history:', error);
    } finally {
      setLoading(false);
    }
  };

  // Transform data for charts
  const clearSearchHistory = () => {
    if (window.confirm('Clear all search history?')) {
      if (user?.id) {
        setSearchHistory([]);
        localStorage.removeItem(`search_history_${user.id}`);
      }
    }
  };

  const clearViewHistory = () => {
    if (window.confirm('Clear all view history?')) {
      if (user?.id) {
        setViewHistory([]);
        localStorage.removeItem(`view_history_${user.id}`);
      }
    }
  };

  const removeSearchItem = (query: string) => {
    const updated = searchHistory.filter(item => item.query !== query);
    setSearchHistory(updated);
    if (user?.id) {
      localStorage.setItem(`search_history_${user.id}`, JSON.stringify(updated));
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);

    if (diffMins < 1) return 'just now';
    if (diffMins < 60) return `${diffMins}m ago`;
    if (diffHours < 24) return `${diffHours}h ago`;
    if (diffDays < 7) return `${diffDays}d ago`;
    
    return date.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric'
    });
  };

  if (loading) {
    return <div className="text-center py-20 text-slate-400">Loading history...</div>;
  }

  return (
    <div className="max-w-7xl mx-auto">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-white mb-2">📜 History</h1>
        <p className="text-slate-400">Your search and view history</p>
      </div>

      {/* Tabs */}
      <div className="flex gap-4 mb-6 border-b border-slate-700">
        <button
          onClick={() => setActiveTab('search')}
          className={`px-4 py-3 font-medium transition-colors ${
            activeTab === 'search'
              ? 'text-indigo-400 border-b-2 border-indigo-400'
              : 'text-slate-400 hover:text-slate-300'
          }`}
        >
          <div className="flex items-center gap-2">
            <SearchIcon size={18} />
            Search History ({searchHistory.length})
          </div>
        </button>
        <button
          onClick={() => setActiveTab('views')}
          className={`px-4 py-3 font-medium transition-colors ${
            activeTab === 'views'
              ? 'text-indigo-400 border-b-2 border-indigo-400'
              : 'text-slate-400 hover:text-slate-300'
          }`}
        >
          <div className="flex items-center gap-2">
            <Calendar size={18} />
            Recently Viewed ({viewHistory.length})
          </div>
        </button>
      </div>

      {activeTab === 'search' ? (
        <div className="space-y-4">
          {searchHistory.length > 0 && (
            <div className="flex justify-end mb-4">
              <button
                onClick={clearSearchHistory}
                className="px-4 py-2 bg-red-600/20 text-red-400 hover:bg-red-600/30 border border-red-500/30 rounded-lg transition-colors"
              >
                Clear All
              </button>
            </div>
          )}

          {searchHistory.length > 0 ? (
            <div className="space-y-2">
              {searchHistory.map((item, index) => (
                <div
                  key={index}
                  className="flex items-center justify-between p-4 bg-slate-800/40 border border-slate-700 rounded-lg hover:border-indigo-500/50 transition-colors"
                >
                  <div className="flex-1">
                    <p className="font-medium text-white">{item.query}</p>
                    <p className="text-sm text-slate-400">{item.count} results • {formatDate(item.timestamp)}</p>
                  </div>
                  <button
                    onClick={() => removeSearchItem(item.query)}
                    className="p-2 text-slate-400 hover:text-red-400 transition-colors"
                  >
                    <Trash2 size={18} />
                  </button>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-12 bg-slate-800/30 rounded-2xl border border-dashed border-slate-700">
              <p className="text-slate-400">No search history yet</p>
            </div>
          )}
        </div>
      ) : (
        <div className="space-y-4">
          {viewHistory.length > 0 && (
            <div className="flex justify-end mb-4">
              <button
                onClick={clearViewHistory}
                className="px-4 py-2 bg-red-600/20 text-red-400 hover:bg-red-600/30 border border-red-500/30 rounded-lg transition-colors"
              >
                Clear All
              </button>
            </div>
          )}

          {viewHistory.length > 0 ? (
            <div className="space-y-2">
              {viewHistory.map((item, index) => (
                <div
                  key={index}
                  className="flex items-center justify-between p-4 bg-slate-800/40 border border-slate-700 rounded-lg hover:border-indigo-500/50 transition-colors"
                >
                  <div className="flex-1">
                    <p className="font-medium text-white">{item.title}</p>
                    <p className="text-sm text-slate-400">{item.content_type} • {formatDate(item.timestamp)}</p>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-12 bg-slate-800/30 rounded-2xl border border-dashed border-slate-700">
              <p className="text-slate-400">No view history yet</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default History;