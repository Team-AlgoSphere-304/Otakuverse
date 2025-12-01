import React, { useState, useEffect } from 'react';
import { RecommendationItem } from '../types';
import { CONTENT_TYPE_LABELS } from '../constants';
import { Star, Bookmark, Info, RotateCw, Check, Loader } from 'lucide-react';
import { recommendationService } from '../services/api';
import { useAuthStore } from '../store/useStore';
import OptimizedImage from './OptimizedImage';

interface Props {
  item: RecommendationItem;
  onRate?: (id: string, rating: number) => void;
}

const RecommendationCard: React.FC<Props> = ({ item, onRate }) => {
  const [isFlipped, setIsFlipped] = useState(false);
  const [userRating, setUserRating] = useState<number>(item.user_rating || 0);
  const [ratingLoading, setRatingLoading] = useState(false);
  const [isSaved, setIsSaved] = useState(false);
  const user = useAuthStore(state => state.user);

  const handleRate = async (e: React.MouseEvent, rating: number) => {
    e.stopPropagation();
    if (!user) return;
    try {
      setRatingLoading(true);
      await recommendationService.rateRecommendation({
        user_id: user.id,
        item_id: item.id,
        rating: rating
      });
      setUserRating(rating);
      if (onRate) onRate(item.id, rating);
    } catch (e) {
      console.error(e);
    } finally {
      setRatingLoading(false);
    }
  };

  const handleSave = (e: React.MouseEvent) => {
    e.stopPropagation();
    setIsSaved(!isSaved);
  };

  const getBadgeColor = (type: string) => {
    switch (type) {
      case 'anime': return 'bg-pink-600';
      case 'manga': return 'bg-orange-500';
      case 'movies': return 'bg-red-600';
      default: return 'bg-indigo-600';
    }
  };

  return (
    <div className="group relative h-[460px] w-full">
      <div className={`relative w-full h-full transition-all duration-700 ${isFlipped ? 'rotate-y-180' : ''}`}>
        
        {/* Front Face */}
        <div className="absolute w-full h-full bg-slate-900 rounded-xl overflow-hidden shadow-2xl border border-slate-800 group-hover:border-indigo-500/50">
          
          {/* Image with OptimizedImage component */}
          <div className="absolute inset-0">
            <OptimizedImage
              src={item.cover_image}
              alt={item.title}
              title={item.title}
              className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700"
            />
            <div className="absolute inset-0 bg-gradient-to-t from-slate-950 via-slate-950/40 to-transparent opacity-80 group-hover:opacity-95 transition-opacity" />
          </div>

          {/* Top Labels */}
          <div className="absolute top-3 left-3 z-10">
            <span className={`${getBadgeColor(item.content_type)} text-white text-[10px] font-bold px-2 py-1 rounded-full uppercase`}>
              {CONTENT_TYPE_LABELS[item.content_type]}
            </span>
          </div>
          
          <div className="absolute top-3 right-3 z-10">
            <div className="bg-slate-950/70 text-yellow-400 text-xs font-bold px-2 py-1 rounded-full flex items-center gap-1">
              <Star size={12} fill="currentColor" />
              {item.rating_score}
            </div>
          </div>

          {/* Bottom Content */}
          <div className="absolute bottom-0 left-0 w-full p-4 z-20">
            <h3 className="text-xl font-bold text-white mb-2 line-clamp-2">{item.title}</h3>
            
            <div className="flex flex-wrap gap-2 mb-1">
              {item.mal_score && (
                <span className="text-[10px] font-bold px-1.5 py-0.5 bg-[#2e51a2] text-white rounded">
                  MAL {item.mal_score}
                </span>
              )}
              {item.imdb_score && (
                <span className="text-[10px] font-bold px-1.5 py-0.5 bg-[#f5c518] text-black rounded">
                  IMDb {item.imdb_score}
                </span>
              )}
              {item.genres.slice(0, 2).map(g => (
                <span key={g} className="text-[10px] text-slate-300 border border-slate-600/50 px-1.5 py-0.5 rounded">
                  {g}
                </span>
              ))}
            </div>

            {/* Hidden on Hover */}
            <div className="group-hover:flex hidden flex-col gap-3 pt-3">
              
              {/* Rating */}
              <div className="bg-slate-900/80 p-2.5 rounded-lg border border-slate-700/50">
                <div className="flex justify-between mb-1">
                  <span className="text-[10px] font-bold text-slate-400">Rating</span>
                  <span className="text-xs font-bold text-yellow-400">{userRating || '-'}/5</span>
                </div>
                <div className="flex gap-1">
                  {[1, 2, 3, 4, 5].map((star) => (
                    <button
                      key={star}
                      onClick={(e) => handleRate(e, star)}
                      className={`transition-all hover:scale-125 ${userRating >= star ? 'text-yellow-400' : 'text-slate-600'}`}
                    >
                      <Star size={16} fill={userRating >= star ? "currentColor" : "none"} />
                    </button>
                  ))}
                </div>
              </div>

              {/* Actions */}
              <div className="flex gap-2">
                <button 
                  onClick={(e) => { e.stopPropagation(); setIsFlipped(true); }}
                  className="flex-1 bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold py-2 rounded-lg flex items-center justify-center gap-1"
                >
                  <Info size={14} />
                  Why?
                </button>
                <button 
                  onClick={handleSave}
                  className={`flex-1 text-xs font-bold py-2 rounded-lg flex items-center justify-center gap-1 ${
                    isSaved 
                    ? 'bg-emerald-600 text-white' 
                    : 'bg-slate-800 text-slate-200 hover:bg-slate-700'
                  }`}
                >
                  {isSaved ? <Check size={14} /> : <Bookmark size={14} />}
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Back Face */}
        <div className="absolute w-full h-full rotate-y-180 bg-slate-900 rounded-xl overflow-hidden shadow-2xl border border-slate-700 p-5 flex flex-col">
          <div className="flex justify-between items-start mb-3 pb-3 border-b border-slate-800">
            <h4 className="text-lg font-bold text-indigo-400 flex items-center gap-2">
              <Info size={16} />
              Details
            </h4>
            <button 
              onClick={(e) => { e.stopPropagation(); setIsFlipped(false); }}
              className="p-1 hover:bg-slate-800 rounded text-slate-400"
            >
              <RotateCw size={14} />
            </button>
          </div>

          <div className="flex-grow overflow-y-auto">
            <p className="text-slate-200 text-sm italic mb-3">{item.explanation}</p>
            <p className="text-slate-400 text-xs">{item.description}</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RecommendationCard;