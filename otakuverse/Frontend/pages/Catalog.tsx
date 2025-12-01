import React, { useEffect, useState } from 'react';
import { catalogService } from '../services/api';
import { RecommendationItem, ContentType } from '../types';
import RecommendationCard from '../components/RecommendationCard';
import { CONTENT_TYPE_LABELS } from '../constants';
import { Search, Filter } from 'lucide-react';

const Catalog: React.FC = () => {
  const [items, setItems] = useState<RecommendationItem[]>([]);
  const [filteredItems, setFilteredItems] = useState<RecommendationItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [activeFilter, setActiveFilter] = useState<ContentType | 'ALL'>('ALL');

  useEffect(() => {
    loadCatalog();
  }, []);

  useEffect(() => {
    let result = items;
    
    if (activeFilter !== 'ALL') {
      result = result.filter(item => item.content_type === activeFilter);
    }

    if (searchTerm) {
      const lower = searchTerm.toLowerCase();
      result = result.filter(item => 
        item.title.toLowerCase().includes(lower) || 
        item.genres.some(g => g.toLowerCase().includes(lower))
      );
    }

    setFilteredItems(result);
  }, [items, searchTerm, activeFilter]);

  const loadCatalog = async () => {
    setLoading(true);
    try {
      const data = await catalogService.getAll();
      setItems(data);
    } catch (e) {
      console.error("Failed to load catalog", e);
      // Fallback empty
      setItems([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <h1 className="text-3xl font-bold text-white">Full Catalog</h1>
        
        {/* Search */}
        <div className="relative w-full md:w-64">
          <input
            type="text"
            placeholder="Search titles or genres..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full bg-slate-800 border border-slate-700 rounded-lg pl-10 pr-4 py-2 text-white focus:outline-none focus:border-indigo-500"
          />
          <Search className="absolute left-3 top-2.5 text-slate-500" size={18} />
        </div>
      </div>

      {/* Filter Tabs */}
      <div className="flex overflow-x-auto pb-2 gap-2 custom-scrollbar">
        <button
          onClick={() => setActiveFilter('ALL')}
          className={`px-4 py-2 rounded-full text-sm font-medium whitespace-nowrap transition-colors ${
            activeFilter === 'ALL' 
              ? 'bg-white text-slate-900' 
              : 'bg-slate-800 text-slate-400 hover:bg-slate-700'
          }`}
        >
          All Content
        </button>
        {Object.values(ContentType).map(type => (
          <button
            key={type}
            onClick={() => setActiveFilter(type)}
            className={`px-4 py-2 rounded-full text-sm font-medium whitespace-nowrap transition-colors ${
              activeFilter === type 
                ? 'bg-indigo-600 text-white' 
                : 'bg-slate-800 text-slate-400 hover:bg-slate-700'
            }`}
          >
            {CONTENT_TYPE_LABELS[type]}
          </button>
        ))}
      </div>

      {/* Grid */}
      {loading ? (
        <div className="text-center py-20 text-slate-500">Loading catalog...</div>
      ) : filteredItems.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {filteredItems.map(item => (
            <RecommendationCard key={item.id} item={item} />
          ))}
        </div>
      ) : (
        <div className="text-center py-20 bg-slate-800/30 rounded-2xl border border-dashed border-slate-700">
          <Filter className="mx-auto text-slate-600 mb-4" size={32} />
          <p className="text-slate-400">No items found matching your search.</p>
        </div>
      )}
    </div>
  );
};

export default Catalog;