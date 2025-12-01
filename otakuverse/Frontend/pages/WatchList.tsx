import React, { useState, useEffect } from 'react';
import { useAuthStore } from '../store/useStore';
import { Trash2, ExternalLink, Clock } from 'lucide-react';

interface WatchListItem {
  content_id: string;
  title: string;
  content_type: string;
  cover_image: string;
  genres: string[];
  rating: number;
  added_at: string;
  episodes?: number;
  description?: string;
}

const WatchList: React.FC = () => {
  const [watchList, setWatchList] = useState<WatchListItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [selectedItem, setSelectedItem] = useState<WatchListItem | null>(null);
  const { user } = useAuthStore();

  useEffect(() => {
    loadWatchList();
  }, [user?.id]);

  const loadWatchList = async () => {
    if (!user?.id) return;
    setLoading(true);
    try {
      const saved = localStorage.getItem(`watchlist_${user.id}`);
      if (saved) {
        setWatchList(JSON.parse(saved));
      }
    } catch (error) {
      console.error('Failed to load watch list:', error);
    } finally {
      setLoading(false);
    }
  };

  const removeFromWatchList = (contentId: string) => {
    if (!user?.id) return;
    const updated = watchList.filter(item => item.content_id !== contentId);
    setWatchList(updated);
    localStorage.setItem(`watchlist_${user.id}`, JSON.stringify(updated));
  };

  const clearAll = () => {
    if (window.confirm('Clear all items from watch list?')) {
      if (user?.id) {
        setWatchList([]);
        localStorage.removeItem(`watchlist_${user.id}`);
      }
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric'
    });
  };

  return (
    <div className="max-w-7xl mx-auto">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-white mb-2">📋 Watch List</h1>
        <p className="text-slate-400">Items you want to watch later ({watchList.length})</p>
      </div>

      {loading ? (
        <div className="text-center py-12">
          <p className="text-slate-400">Loading...</p>
        </div>
      ) : watchList.length > 0 ? (
        <div className="space-y-4">
          {/* Clear All Button */}
          <div className="flex justify-end mb-4">
            <button
              onClick={clearAll}
              className="px-4 py-2 bg-red-600/20 text-red-400 hover:bg-red-600/30 border border-red-500/30 rounded-lg transition-colors"
            >
              Clear All
            </button>
          </div>

          {/* Watch List Items */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {watchList.map((item) => (
              <div
                key={item.content_id}
                className="bg-slate-800/60 border border-slate-700 rounded-lg overflow-hidden hover:border-indigo-500/50 transition-all group cursor-pointer"
                onClick={() => setSelectedItem(item)}
              >
                <div className="relative overflow-hidden h-48 bg-slate-900">
                  <img
                    src={item.cover_image || 'https://via.placeholder.com/300x400?text=No+Image'}
                    alt={item.title}
                    className="w-full h-full object-cover group-hover:scale-110 transition-transform"
                    onError={(e) => {
                      (e.target as HTMLImageElement).src =
                        'https://via.placeholder.com/300x400?text=No+Image';
                    }}
                  />
                  <div className="absolute top-2 right-2 flex gap-2">
                    <span className="px-2 py-1 bg-indigo-600/80 text-white text-xs rounded">
                      {item.content_type}
                    </span>
                    {item.rating > 0 && (
                      <span className="px-2 py-1 bg-yellow-600/80 text-white text-xs rounded flex items-center gap-1">
                        ⭐ {item.rating.toFixed(1)}
                      </span>
                    )}
                  </div>
                </div>

                <div className="p-4">
                  <h3 className="font-semibold text-white mb-2 line-clamp-2">{item.title}</h3>
                  
                  {item.genres && item.genres.length > 0 && (
                    <div className="flex flex-wrap gap-1 mb-3">
                      {item.genres.slice(0, 2).map((genre) => (
                        <span
                          key={genre}
                          className="text-xs bg-slate-700/50 text-slate-300 px-2 py-1 rounded"
                        >
                          {genre}
                        </span>
                      ))}
                      {item.genres.length > 2 && (
                        <span className="text-xs text-slate-400">+{item.genres.length - 2}</span>
                      )}
                    </div>
                  )}

                  <div className="flex items-center justify-between text-xs text-slate-400 mb-3">
                    <div className="flex items-center gap-1">
                      <Clock size={14} />
                      {formatDate(item.added_at)}
                    </div>
                  </div>

                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      removeFromWatchList(item.content_id);
                    }}
                    className="w-full py-2 bg-red-600/20 hover:bg-red-600/30 text-red-400 rounded transition-colors flex items-center justify-center gap-2"
                  >
                    <Trash2 size={16} />
                    Remove
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      ) : (
        <div className="text-center py-20 bg-slate-800/30 rounded-2xl border border-dashed border-slate-700">
          <h3 className="text-xl font-medium text-slate-300 mb-2">No items in watch list</h3>
          <p className="text-slate-500 mb-4">Start searching for anime and add items to watch later</p>
        </div>
      )}

      {/* Detail Modal */}
      {selectedItem && (
        <div
          className="fixed inset-0 bg-black/80 flex items-center justify-center z-50 p-4"
          onClick={() => setSelectedItem(null)}
        >
          <div
            className="bg-slate-800 rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="sticky top-0 flex justify-between items-center p-4 border-b border-slate-700 bg-slate-850">
              <h2 className="text-xl font-bold text-white">{selectedItem.title}</h2>
              <button
                onClick={() => setSelectedItem(null)}
                className="text-slate-400 hover:text-white text-2xl"
              >
                ✕
              </button>
            </div>

            <div className="p-6 space-y-4">
              <div className="flex gap-4">
                <img
                  src={selectedItem.cover_image}
                  alt={selectedItem.title}
                  className="w-40 h-56 object-cover rounded"
                  onError={(e) => {
                    (e.target as HTMLImageElement).src =
                      'https://via.placeholder.com/300x400?text=No+Image';
                  }}
                />

                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-3">
                    <span className="px-3 py-1 bg-indigo-600/30 text-indigo-300 rounded-full text-sm font-medium">
                      {selectedItem.content_type}
                    </span>
                    {selectedItem.rating > 0 && (
                      <span className="text-lg">⭐ {selectedItem.rating.toFixed(1)}/10</span>
                    )}
                  </div>

                  {selectedItem.episodes && (
                    <p className="text-slate-400 mb-2">
                      <span className="font-semibold">Episodes:</span> {selectedItem.episodes}
                    </p>
                  )}

                  {selectedItem.genres && selectedItem.genres.length > 0 && (
                    <div className="mb-4">
                      <p className="font-semibold text-slate-300 mb-2">Genres:</p>
                      <div className="flex flex-wrap gap-2">
                        {selectedItem.genres.map((genre) => (
                          <span
                            key={genre}
                            className="px-3 py-1 bg-slate-700/50 text-slate-300 rounded-full text-sm"
                          >
                            {genre}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}

                  <p className="text-slate-400 text-sm mb-3">
                    Added: {formatDate(selectedItem.added_at)}
                  </p>

                  <button
                    onClick={() => {
                      removeFromWatchList(selectedItem.content_id);
                      setSelectedItem(null);
                    }}
                    className="w-full py-2 bg-red-600/20 hover:bg-red-600/30 text-red-400 rounded transition-colors"
                  >
                    Remove from Watch List
                  </button>
                </div>
              </div>

              {selectedItem.description && (
                <div className="pt-4 border-t border-slate-700">
                  <h3 className="font-semibold text-slate-300 mb-2">Synopsis</h3>
                  <p className="text-slate-400 text-sm leading-relaxed">
                    {selectedItem.description}
                  </p>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default WatchList;
