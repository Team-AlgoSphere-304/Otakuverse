import React, { useState } from 'react';
import ContentTypeSelector from '../components/ContentTypeSelector';
import PreferenceForm from '../components/PreferenceForm';
import RecommendationCard from '../components/RecommendationCard';
import LoadingScreen from '../components/LoadingScreen';
import { ContentType, Mood, StylePreference, RecommendationItem } from '../types';
import { recommendationService } from '../services/api';
import { useAuthStore, useAppStore } from '../store/useStore';
import { Sparkles, RefreshCw, AlertTriangle, MessageSquare } from 'lucide-react';

const Recommendations: React.FC = () => {
  const [step, setStep] = useState<1 | 2>(1);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Form State
  const [selectedTypes, setSelectedTypes] = useState<ContentType[]>([]);
  const [mood, setMood] = useState<Mood>(Mood.HAPPY);
  const [selectedGenres, setSelectedGenres] = useState<string[]>([]);
  const [stylePreference, setStylePreference] = useState<StylePreference>(StylePreference.MAINSTREAM);
  const [customPrompt, setCustomPrompt] = useState('');

  const { user } = useAuthStore();
  const { recommendations, setRecommendations } = useAppStore();

  const handleGetRecommendations = async () => {
    if (selectedTypes.length === 0) {
      setError("Please select at least one content type.");
      return;
    }
    if (!user) return;

    setLoading(true);
    setError(null);
    try {
      const data = await recommendationService.getRecommendations({
        user_id: user.id,
        mood,
        content_types: selectedTypes,
        genres: selectedGenres,
        preferred_style: stylePreference,
        custom_prompt: customPrompt
      });
      setRecommendations(data);
      setStep(2);
    } catch (err: any) {
      console.error(err);
      setError("Failed to fetch recommendations. Please ensure the backend is running.");
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setStep(1);
    setRecommendations([]);
  };

  return (
    <div className="max-w-7xl mx-auto">
      {loading && <LoadingScreen />}
      
      {/* Header */}
      <div className="mb-8 animate-fade-in-down">
        <h1 className="text-4xl font-bold text-white mb-2 tracking-tight">
          {step === 1 ? 'Configure Your Experience' : 'Your Personal Picks'}
        </h1>
        <p className="text-slate-400 text-lg">
          {step === 1 
            ? 'Tell us what you are looking for, and our agents will do the rest.' 
            : `We found ${recommendations.length} items that match your vibe.`}
        </p>
      </div>

      {step === 1 && (
        <div className="space-y-8">
          <section className="animate-fade-in-up" style={{ animationDelay: '0.1s' }}>
            <ContentTypeSelector 
              selectedTypes={selectedTypes} 
              onChange={(types) => {
                setSelectedTypes(types);
                if (types.length > 0) setError(null);
              }} 
            />
          </section>

          <section className="animate-fade-in-up" style={{ animationDelay: '0.2s' }}>
            <PreferenceForm 
              mood={mood} 
              setMood={setMood}
              selectedGenres={selectedGenres} 
              setSelectedGenres={setSelectedGenres}
              stylePreference={stylePreference}
              setStylePreference={setStylePreference}
              customPrompt={customPrompt}
              setCustomPrompt={setCustomPrompt}
            />
          </section>

          {error && (
            <div className="p-4 bg-red-900/30 border border-red-500/50 rounded-lg flex items-center gap-3 text-red-200 animate-pop">
              <AlertTriangle size={20} />
              <span>{error}</span>
            </div>
          )}

          <div className="flex justify-end pt-4 animate-fade-in-up" style={{ animationDelay: '0.3s' }}>
            <button
              onClick={handleGetRecommendations}
              disabled={loading}
              className={`
                relative overflow-hidden
                bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 
                text-white font-bold py-4 px-12 rounded-xl shadow-[0_0_20px_rgba(99,102,241,0.4)]
                transition-all transform hover:scale-[1.02] hover:-translate-y-1 active:scale-[0.98]
                flex items-center gap-3 text-lg
                ${loading ? 'opacity-70 cursor-not-allowed' : ''}
              `}
            >
               {/* Shine effect */}
               <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent -translate-x-full hover:animate-[shimmer_1s_infinite]" />
              
              {loading ? (
                <>
                  <RefreshCw className="animate-spin" /> Analyzing...
                </>
              ) : (
                <>
                  <Sparkles className="animate-pulse" /> Generate Recommendations
                </>
              )}
            </button>
          </div>
        </div>
      )}

      {step === 2 && (
        <div className="space-y-8">
          <div className="flex flex-col gap-3 bg-slate-800/60 backdrop-blur-md p-4 rounded-xl border border-slate-700 animate-fade-in-down">
            <div className="flex justify-between items-center">
              <div className="flex gap-2 flex-wrap text-sm text-slate-300">
                <span className="px-2 py-1 bg-slate-800 rounded border border-slate-600">{mood}</span>
                <span className="px-2 py-1 bg-slate-800 rounded border border-slate-600">{stylePreference}</span>
                {selectedTypes.map(t => (
                  <span key={t} className="px-2 py-1 bg-indigo-900/40 rounded border border-indigo-500/30 text-indigo-300">{t}</span>
                ))}
              </div>
              <button 
                onClick={handleReset}
                className="text-slate-400 hover:text-white flex items-center gap-2 text-sm font-medium transition-colors"
              >
                <RefreshCw size={16} />
                Adjust Preferences
              </button>
            </div>
            
            {customPrompt && (
              <div className="flex items-start gap-2 bg-indigo-900/20 border border-indigo-500/20 p-3 rounded-lg text-sm text-indigo-200">
                <MessageSquare size={16} className="mt-0.5 shrink-0 text-indigo-400" />
                <p><span className="font-bold text-indigo-400">Custom Request:</span> "{customPrompt}"</p>
              </div>
            )}
          </div>

          {recommendations.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
              {recommendations.map((item, index) => (
                <div 
                  key={item.id} 
                  className="animate-pop opacity-0" 
                  style={{ animationDelay: `${index * 100}ms`, animationFillMode: 'forwards' }}
                >
                  <RecommendationCard item={item} />
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-20 bg-slate-800/30 rounded-2xl border border-dashed border-slate-700 animate-fade-in-up">
              <h3 className="text-xl font-medium text-slate-300 mb-2">No recommendations found</h3>
              <p className="text-slate-500">Try adjusting your filters to be less specific.</p>
              <button onClick={handleReset} className="mt-4 text-indigo-400 hover:text-indigo-300">
                Go Back
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default Recommendations;