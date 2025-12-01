import React from 'react';
import { ContentType } from '../types';
import { CONTENT_TYPE_LABELS } from '../constants';
import { 
  Tv, Film, BookOpen, Gamepad2, Layers, Book, MonitorPlay 
} from 'lucide-react';

interface ContentTypeSelectorProps {
  selectedTypes: ContentType[];
  onChange: (types: ContentType[]) => void;
}

const ICONS: Record<ContentType, React.ReactNode> = {
  [ContentType.ANIME]: <Tv size={24} />,
  [ContentType.MOVIES]: <Film size={24} />,
  [ContentType.WEB_SERIES]: <MonitorPlay size={24} />,
  [ContentType.MANGA]: <BookOpen size={24} />,
  [ContentType.MANHWA]: <Layers size={24} />,
  [ContentType.COMICS]: <BookOpen size={24} />, // Reusing BookOpen for simplicity
  [ContentType.GAMES]: <Gamepad2 size={24} />,
  [ContentType.LIGHT_NOVELS]: <Book size={24} />,
  [ContentType.NOVELS]: <Book size={24} />,
};

const ContentTypeSelector: React.FC<ContentTypeSelectorProps> = ({ selectedTypes, onChange }) => {
  const toggleType = (type: ContentType) => {
    if (selectedTypes.includes(type)) {
      onChange(selectedTypes.filter(t => t !== type));
    } else {
      onChange([...selectedTypes, type]);
    }
  };

  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <label className="text-xl font-bold text-slate-200">
          What are you interested in?
        </label>
        <span className="text-sm font-medium bg-indigo-900/50 text-indigo-300 px-3 py-1 rounded-full border border-indigo-500/30 shadow-sm">
          {selectedTypes.length}/9 selected
        </span>
      </div>
      
      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-3">
        {Object.values(ContentType).map((type) => {
          const isSelected = selectedTypes.includes(type);
          return (
            <button
              key={type}
              type="button"
              onClick={() => toggleType(type)}
              className={`
                relative flex flex-col items-center justify-center p-4 rounded-xl border-2 transition-all duration-300 group
                ${isSelected 
                  ? 'border-indigo-500 bg-indigo-500/10 text-indigo-300 shadow-[0_0_15px_rgba(99,102,241,0.2)] scale-105 animate-pop' 
                  : 'border-slate-700 bg-slate-800/50 text-slate-400 hover:border-slate-500 hover:bg-slate-800 hover:-translate-y-1'}
              `}
            >
              <div className={`mb-2 transition-transform duration-300 ${isSelected ? 'text-indigo-400 scale-110' : 'text-slate-500 group-hover:scale-110'}`}>
                {ICONS[type]}
              </div>
              <span className="text-sm font-medium">{CONTENT_TYPE_LABELS[type]}</span>
              
              {isSelected && (
                <div className="absolute top-2 right-2 w-2 h-2 bg-indigo-400 rounded-full animate-pulse shadow-[0_0_8px_rgba(99,102,241,0.8)]" />
              )}
            </button>
          );
        })}
      </div>
      {selectedTypes.length === 0 && (
        <p className="text-red-400 text-sm mt-2 animate-pulse flex items-center gap-1">
          <span>*</span> Please select at least one content type
        </p>
      )}
    </div>
  );
};

export default ContentTypeSelector;