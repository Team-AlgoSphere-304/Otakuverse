import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { User, RecommendationItem, HistoryItem } from '../types';
import { authService } from '../services/api';

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (token: string, user: User) => void;
  logout: () => void;
  updateUser: (user: User) => void;
}

interface AppState {
  recommendations: RecommendationItem[];
  history: HistoryItem[];
  loading: boolean;
  error: string | null;
  selectedContentTypes: string[];
  currentMood: string;
  currentGenres: string[];
  preferredStyle: string;
  
  setRecommendations: (items: RecommendationItem[]) => void;
  setHistory: (items: HistoryItem[]) => void;
  addToHistory: (item: HistoryItem) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  setSelectedContentTypes: (types: string[]) => void;
  setCurrentMood: (mood: string) => void;
  setCurrentGenres: (genres: string[]) => void;
  setPreferredStyle: (style: string) => void;
  updateRecommendation: (id: string, updates: Partial<RecommendationItem>) => void;
  clearRecommendations: () => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => {
      const storedToken = localStorage.getItem('auth_token');
      const storedUser = localStorage.getItem('user_data');
      
      return {
        token: storedToken,
        user: storedUser ? JSON.parse(storedUser) : null,
        isAuthenticated: !!storedToken,
        isLoading: false,
        login: (token, user) => {
          localStorage.setItem('auth_token', token);
          localStorage.setItem('user_data', JSON.stringify(user));
          set({ token, user, isAuthenticated: true });
        },
        logout: () => {
          localStorage.removeItem('auth_token');
          localStorage.removeItem('user_data');
          set({ token: null, user: null, isAuthenticated: false });
        },
        updateUser: (user) => {
          localStorage.setItem('user_data', JSON.stringify(user));
          set({ user });
        }
      };
    },
    {
      name: 'auth-store'
    }
  )
);

export const useAppStore = create<AppState>()(
  persist(
    (set) => ({
      recommendations: [],
      history: [],
      loading: false,
      error: null,
      selectedContentTypes: [],
      currentMood: '',
      currentGenres: [],
      preferredStyle: '',
      
      setRecommendations: (items) => set({ recommendations: items }),
      setHistory: (items) => set({ history: items }),
      addToHistory: (item) => set((state) => ({ history: [item, ...state.history] })),
      setLoading: (loading) => set({ loading }),
      setError: (error) => set({ error }),
      setSelectedContentTypes: (types) => set({ selectedContentTypes: types }),
      setCurrentMood: (mood) => set({ currentMood: mood }),
      setCurrentGenres: (genres) => set({ currentGenres: genres }),
      setPreferredStyle: (style) => set({ preferredStyle: style }),
      updateRecommendation: (id, updates) => set((state) => ({
        recommendations: state.recommendations.map((rec) =>
          rec.id === id ? { ...rec, ...updates } : rec
        ),
      })),
      clearRecommendations: () => set({ recommendations: [] }),
    }),
    {
      name: 'app-store',
      partialize: (state) => ({
        history: state.history,
        selectedContentTypes: state.selectedContentTypes,
        currentMood: state.currentMood,
        currentGenres: state.currentGenres,
        preferredStyle: state.preferredStyle,
      })
    }
  )
);
