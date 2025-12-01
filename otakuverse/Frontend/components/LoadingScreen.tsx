import React from 'react';
import { Loader, Sparkles, Database, Zap } from 'lucide-react';

interface LoadingScreenProps {
  message?: string;
  progress?: number;
}

const LoadingScreen: React.FC<LoadingScreenProps> = ({ message = "Fetching fresh recommendations...", progress = 0 }) => {
  return (
    <div className="fixed inset-0 bg-slate-900/95 backdrop-blur-md flex items-center justify-center z-50">
      <div className="text-center">
        {/* Animated loader */}
        <div className="mb-8 flex justify-center">
          <div className="relative w-32 h-32">
            {/* Outer rotating ring */}
            <div className="absolute inset-0 rounded-full border-4 border-slate-700 border-t-indigo-500 animate-spin" />
            
            {/* Middle ring */}
            <div className="absolute inset-2 rounded-full border-2 border-slate-700 border-b-purple-500" style={{
              animation: 'spin 2s linear reverse'
            }} />
            
            {/* Inner icon */}
            <div className="absolute inset-0 flex items-center justify-center">
              <Sparkles className="w-12 h-12 text-indigo-400 animate-pulse" />
            </div>
          </div>
        </div>

        {/* Main message */}
        <h2 className="text-2xl font-bold text-white mb-2">{message}</h2>
        <p className="text-slate-400 mb-8">Getting real data from MAL & IMDb APIs...</p>

        {/* Progress bar */}
        <div className="w-64 h-2 bg-slate-800 rounded-full overflow-hidden mb-6">
          <div 
            className="h-full bg-gradient-to-r from-indigo-500 to-purple-500 transition-all duration-500"
            style={{ width: `${progress}%` }}
          />
        </div>

        {/* Status indicators */}
        <div className="space-y-3 text-left max-w-sm mx-auto">
          <div className="flex items-center gap-3 text-slate-300">
            <Database className="w-5 h-5 text-indigo-400 animate-pulse" />
            <span>Querying databases...</span>
          </div>
          <div className="flex items-center gap-3 text-slate-300">
            <Zap className="w-5 h-5 text-purple-400 animate-pulse" style={{ animationDelay: '0.2s' }} />
            <span>Processing results...</span>
          </div>
          <div className="flex items-center gap-3 text-slate-300">
            <Sparkles className="w-5 h-5 text-pink-400 animate-pulse" style={{ animationDelay: '0.4s' }} />
            <span>Personalizing for you...</span>
          </div>
        </div>

        {/* Tip */}
        <p className="text-xs text-slate-500 mt-8">This may take 5-15 seconds on first request</p>
      </div>

      <style>{`
        @keyframes spin {
          to { transform: rotate(-360deg); }
        }
      `}</style>
    </div>
  );
};

export default LoadingScreen;
