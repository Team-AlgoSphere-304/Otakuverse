import React from 'react';
import { Link } from 'react-router-dom';
import { useAuthStore } from '../store/useStore';
import { Rocket, Brain, Sparkles, Layers, Zap } from 'lucide-react';

const Home: React.FC = () => {
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);

  return (
    <div className="flex flex-col items-center overflow-hidden">
      {/* Hero Section */}
      <section className="relative w-full max-w-5xl py-24 text-center space-y-8 z-10">
        {/* Background decorative blobs */}
        <div className="absolute top-0 left-1/4 w-72 h-72 bg-purple-600/20 rounded-full blur-[100px] -z-10 animate-pulse-glow"></div>
        <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-indigo-600/10 rounded-full blur-[100px] -z-10 animate-float"></div>

        <div className="inline-flex items-center gap-2 p-2 px-4 rounded-full bg-indigo-900/30 border border-indigo-500/30 text-indigo-300 text-sm font-medium mb-4 animate-fade-in-down shadow-[0_0_15px_rgba(99,102,241,0.3)]">
          <Zap size={14} className="text-yellow-400" />
          <span>Powered by Multi-Agent AI</span>
        </div>
        
        <h1 className="text-5xl md:text-8xl font-extrabold bg-clip-text text-transparent bg-gradient-to-r from-indigo-400 via-purple-400 to-cyan-400 leading-tight animate-fade-in-up" style={{ animationDelay: '0.1s' }}>
          Discover Your Next<br />
          <span className="text-white drop-shadow-[0_0_20px_rgba(168,85,247,0.5)]">Obsession</span>
        </h1>
        
        <p className="text-xl md:text-2xl text-slate-300 max-w-2xl mx-auto leading-relaxed animate-fade-in-up opacity-0" style={{ animationDelay: '0.3s' }}>
          OtakuVerse analyzes your mood, style, and taste across <span className="text-cyan-400 font-semibold">Anime, Manga, Games</span>, and more to find the perfect entertainment match.
        </p>
        
        <div className="flex flex-col sm:flex-row gap-4 justify-center mt-8 animate-fade-in-up opacity-0" style={{ animationDelay: '0.5s' }}>
          {isAuthenticated ? (
            <Link 
              to="/recommendations" 
              className="group relative bg-indigo-600 hover:bg-indigo-500 text-white px-8 py-4 rounded-xl font-bold text-lg shadow-[0_0_20px_rgba(79,70,229,0.4)] transition-all hover:scale-105 hover:-translate-y-1 flex items-center justify-center gap-2 overflow-hidden"
            >
              <div className="absolute inset-0 w-full h-full bg-gradient-to-r from-transparent via-white/20 to-transparent -translate-x-full group-hover:animate-[shimmer_1.5s_infinite]"></div>
              <Sparkles className="group-hover:rotate-12 transition-transform" />
              Get Recommendations
            </Link>
          ) : (
            <>
              <Link 
                to="/register" 
                className="group relative bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white px-8 py-4 rounded-xl font-bold text-lg shadow-[0_0_20px_rgba(147,51,234,0.4)] transition-all hover:scale-105 hover:-translate-y-1 overflow-hidden"
              >
                <div className="absolute inset-0 bg-white/10 opacity-0 group-hover:opacity-100 transition-opacity"></div>
                Start Exploring
              </Link>
              <Link 
                to="/login" 
                className="bg-slate-800 hover:bg-slate-700 text-white px-8 py-4 rounded-xl font-bold text-lg border border-slate-700 hover:border-slate-500 transition-all hover:scale-105 hover:-translate-y-1"
              >
                Login
              </Link>
            </>
          )}
        </div>
      </section>

      {/* Features Grid */}
      <section className="grid md:grid-cols-3 gap-8 max-w-6xl w-full px-4 py-16">
        <div className="bg-slate-800/40 backdrop-blur-sm p-8 rounded-3xl border border-slate-700 hover:border-indigo-500/50 transition-all duration-300 hover:bg-slate-800/60 animate-fade-in-up opacity-0 group hover:shadow-[0_0_30px_rgba(99,102,241,0.15)]" style={{ animationDelay: '0.6s' }}>
          <div className="w-14 h-14 bg-indigo-900/50 rounded-2xl flex items-center justify-center text-indigo-400 mb-6 group-hover:scale-110 group-hover:rotate-3 transition-transform duration-300 shadow-inner shadow-indigo-500/20">
            <Brain size={32} />
          </div>
          <h3 className="text-xl font-bold text-white mb-3">Mood-Based AI</h3>
          <p className="text-slate-400 leading-relaxed">
            Feeling nostalgic? Or maybe adventurous? Our AI agents coordinate to find content that matches your exact emotional state.
          </p>
        </div>
        
        <div className="bg-slate-800/40 backdrop-blur-sm p-8 rounded-3xl border border-slate-700 hover:border-purple-500/50 transition-all duration-300 hover:bg-slate-800/60 animate-fade-in-up opacity-0 group hover:shadow-[0_0_30px_rgba(168,85,247,0.15)]" style={{ animationDelay: '0.7s' }}>
          <div className="w-14 h-14 bg-purple-900/50 rounded-2xl flex items-center justify-center text-purple-400 mb-6 group-hover:scale-110 group-hover:-rotate-3 transition-transform duration-300 shadow-inner shadow-purple-500/20">
            <Layers size={32} />
          </div>
          <h3 className="text-xl font-bold text-white mb-3">Cross-Media Search</h3>
          <p className="text-slate-400 leading-relaxed">
            Don't limit yourself. We search across 9 different media types including Light Novels, Manhwa, and Indie Games.
          </p>
        </div>
        
        <div className="bg-slate-800/40 backdrop-blur-sm p-8 rounded-3xl border border-slate-700 hover:border-cyan-500/50 transition-all duration-300 hover:bg-slate-800/60 animate-fade-in-up opacity-0 group hover:shadow-[0_0_30px_rgba(6,182,212,0.15)]" style={{ animationDelay: '0.8s' }}>
          <div className="w-14 h-14 bg-cyan-900/50 rounded-2xl flex items-center justify-center text-cyan-400 mb-6 group-hover:scale-110 group-hover:rotate-6 transition-transform duration-300 shadow-inner shadow-cyan-500/20">
            <Rocket size={32} />
          </div>
          <h3 className="text-xl font-bold text-white mb-3">Smart Explanations</h3>
          <p className="text-slate-400 leading-relaxed">
            We don't just show you a title. We tell you <em>why</em> you'll love it based on your specific taste profile.
          </p>
        </div>
      </section>

      {/* Stats/Showcase (Mock) */}
      <section className="w-full py-16 border-t border-slate-800/50 bg-slate-950/30 animate-fade-in opacity-0" style={{ animationDelay: '1s' }}>
        <div className="max-w-6xl mx-auto px-4 flex flex-wrap justify-around text-center gap-8">
          <div className="group cursor-default">
            <div className="text-5xl font-bold text-indigo-400 mb-2 group-hover:scale-110 transition-transform duration-300">10k+</div>
            <div className="text-slate-500 font-medium uppercase tracking-wider text-sm">Titles Indexed</div>
          </div>
          <div className="group cursor-default">
            <div className="text-5xl font-bold text-purple-400 mb-2 group-hover:scale-110 transition-transform duration-300">9</div>
            <div className="text-slate-500 font-medium uppercase tracking-wider text-sm">Content Types</div>
          </div>
          <div className="group cursor-default">
            <div className="text-5xl font-bold text-cyan-400 mb-2 group-hover:scale-110 transition-transform duration-300">24/7</div>
            <div className="text-slate-500 font-medium uppercase tracking-wider text-sm">AI Availability</div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;