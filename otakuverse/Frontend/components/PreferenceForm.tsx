import React from 'react';
import { Mood, StylePreference } from '../types';
import { GENRES, MOOD_LABELS, STYLE_LABELS } from '../constants';
import { Smile, Palette, Hash, MessageSquare } from 'lucide-react';

interface PreferenceFormProps {
  mood: Mood;
  setMood: (mood: Mood) => void;
  selectedGenres: string[];
  setSelectedGenres: (genres: string[]) => void;
  stylePreference: StylePreference;
  setStylePreference: (style: StylePreference) => void;
  customPrompt: string;
  setCustomPrompt: (prompt: string) => void;
}

const PreferenceForm: React.FC<PreferenceFormProps> = ({
  mood,
  setMood,
  selectedGenres,
  setSelectedGenres,
  stylePreference,
  setStylePreference,
  customPrompt,
  setCustomPrompt
}) => {
  
  const toggleGenre = (genre: string) => {
    if (selectedGenres.includes(genre)) {
      setSelectedGenres(selectedGenres.filter(g => g !== genre));
    } else {
      setSelectedGenres([...selectedGenres, genre]);
    }
  };

  return (
    <div className="space-y-8 bg-slate-900/50 p-6 rounded-2xl border border-slate-800">
      {/* Mood Section */}
      <div className="space-y-3">
        <div className="flex items-center space-x-2 text-indigo-300 mb-2">
          <Smile size={20} />
          <h3 className="font-semibold text-lg">Current Mood</h3>
        </div>
        <div className="flex flex-wrap gap-2">
          {Object.values(Mood).map((m) => (
            <button
              key={m}
              type="button"
              onClick={() => setMood(m)}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                mood === m
                  ? 'bg-purple-600 text-white shadow-lg shadow-purple-500/30 transform scale-105'
                  : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
              }`}
            >
              {MOOD_LABELS[m]}
            </button>
          ))}
        </div>
      </div>

      {/* Style Preference */}
      <div className="space-y-3">
        <div className="flex items-center space-x-2 text-indigo-300 mb-2">
          <Palette size={20} />
          <h3 className="font-semibold text-lg">Style Preference</h3>
        </div>
        <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
          {Object.values(StylePreference).map((s) => (
            <button
              key={s}
              type="button"
              onClick={() => setStylePreference(s)}
              className={`px-3 py-2 rounded-lg text-sm font-medium border transition-all ${
                stylePreference === s
                  ? 'border-cyan-500 bg-cyan-950/30 text-cyan-300'
                  : 'border-slate-700 bg-transparent text-slate-400 hover:border-slate-600'
              }`}
            >
              {STYLE_LABELS[s]}
            </button>
          ))}
        </div>
      </div>

      {/* Genres */}
      <div className="space-y-3">
        <div className="flex items-center space-x-2 text-indigo-300 mb-2">
          <Hash size={20} />
          <h3 className="font-semibold text-lg">Genres</h3>
        </div>
        <div className="flex flex-wrap gap-2 max-h-48 overflow-y-auto pr-2 custom-scrollbar">
          {GENRES.map((genre) => {
            const isSelected = selectedGenres.includes(genre);
            return (
              <button
                key={genre}
                type="button"
                onClick={() => toggleGenre(genre)}
                className={`px-3 py-1.5 rounded-full text-xs font-medium border transition-colors ${
                  isSelected
                    ? 'bg-pink-600 border-pink-500 text-white'
                    : 'bg-slate-800 border-slate-700 text-slate-400 hover:border-slate-500'
                }`}
              >
                {genre}
              </button>
            );
          })}
        </div>
        <p className="text-xs text-slate-500 text-right">
          {selectedGenres.length} genres selected
        </p>
      </div>

      {/* Custom Prompt */}
      <div className="space-y-3">
        <div className="flex items-center space-x-2 text-indigo-300 mb-2">
          <MessageSquare size={20} />
          <h3 className="font-semibold text-lg">Custom Request (Optional)</h3>
        </div>
        <textarea
          value={customPrompt}
          onChange={(e) => setCustomPrompt(e.target.value)}
          placeholder="e.g., I want an anime with time travel and a complex plot, or a game that feels like Dark Souls..."
          className="w-full bg-slate-800 border border-slate-700 rounded-xl p-4 text-slate-200 placeholder-slate-500 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-all resize-none h-24"
        />
        <p className="text-xs text-slate-500">
          Our AI agents will prioritize this prompt when finding matches for you.
        </p>
      </div>
    </div>
  );
};

export default PreferenceForm;