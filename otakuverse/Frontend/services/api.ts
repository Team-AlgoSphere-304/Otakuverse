import axios from 'axios';
import { AuthResponse, HistoryItem, RateRequest, RecommendationItem, RecommendationRequest, User, ContentType } from '../types';

// Get API URL from environment or use default
const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8001';

console.log('🔧 API_URL configured as:', API_URL);

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 second timeout
});

// Request interceptor
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('auth_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor for better error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    throw error;
  }
);

const delay = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));

export const authService = {
  login: async (email: string, password: string): Promise<AuthResponse> => {
    // MOCK IMPLEMENTATION: Bypass backend
    console.log(`[Mock Auth] Logging in with ${email}`);
    await delay(1000); // Simulate network latency

    // Simulate basic validation or error if needed (optional)
    if (!email || !password) {
       throw { response: { data: { message: 'Email and password required' } } };
    }

    // Return mock successful response
    return {
      token: 'mock-jwt-token-' + Date.now(),
      user: {
        id: 'mock-user-123',
        username: email.split('@')[0],
        email: email,
        preferences: {
          favorite_genres: ['Action', 'Fantasy']
        }
      }
    };

    /* REAL BACKEND CALL - Uncomment to restore
    const response = await api.post<AuthResponse>('/auth/login', { email, password });
    return response.data;
    */
  },

  register: async (username: string, email: string, password: string): Promise<AuthResponse> => {
    // MOCK IMPLEMENTATION: Bypass backend
    console.log(`[Mock Auth] Registering ${username}`);
    await delay(1000);

    return {
      token: 'mock-jwt-token-' + Date.now(),
      user: {
        id: 'mock-user-' + Date.now(),
        username: username,
        email: email,
        preferences: {}
      }
    };

    /* REAL BACKEND CALL - Uncomment to restore
    const response = await api.post<AuthResponse>('/auth/register', { username, email, password });
    return response.data;
    */
  },

  getProfile: async (): Promise<User> => {
    // MOCK IMPLEMENTATION
    // Usually used to validate token on refresh, return mock user
    await delay(500);
    return {
      id: 'mock-user-123',
      username: 'MockUser',
      email: 'mock@example.com'
    };

    /* REAL BACKEND CALL - Uncomment to restore
    const response = await api.get<User>('/auth/profile');
    return response.data;
    */
  },
};

export const recommendationService = {
  getRecommendations: async (data: RecommendationRequest): Promise<RecommendationItem[]> => {
    try {
      const response = await api.post<any>('/recommendations', {
        user_id: data.user_id,
        genres: data.genres || [],
        moods: [data.mood],
        content_types: data.content_types,
        exclude_titles: [],
        count: 15
      }, {
        timeout: 30000 // Increase timeout for API calls (up to 30 seconds)
      });
      
      // Transform backend response to frontend format
      return response.data.recommendations.map((rec: any) => ({
        id: rec.content_id,
        title: rec.title,
        content_type: rec.content_type,
        genres: rec.genres || [],
        description: rec.description || '',
        explanation: rec.description || '',
        rating_score: rec.rating || rec.mal_score || rec.imdb_score || 0,
        mal_score: rec.mal_score || 0,  // Real MAL score from MyAnimeList API
        imdb_score: rec.imdb_score || 0,  // Real IMDb score from OMDb API
        cover_image: rec.cover_image || 'https://via.placeholder.com/300x450?text=No+Image',  // Real image from MAL/IMDb
        user_rating: 0
      }));
    } catch (error) {
      console.error("Error fetching recommendations:", error);
      throw error;
    }
  },
  rateRecommendation: async (data: RateRequest): Promise<void> => {
    try {
      await api.post('/recommendations/rate', data);
    } catch (error) {
      console.error("Error rating recommendation:", error);
    }
  },
  getHistory: async (userId: string): Promise<HistoryItem[]> => {
    try {
      const response = await api.get<HistoryItem[]>(`/recommendations/history/${userId}`);
      return response.data;
    } catch (error) {
      console.error("Error fetching history:", error);
      return [];
    }
  },
};

export const catalogService = {
  getAll: async (): Promise<RecommendationItem[]> => {
    try {
      const response = await api.get<RecommendationItem[]>('/catalog/all');
      return response.data;
    } catch (error) {
      console.error("Error fetching catalog:", error);
      throw error;
    }
  },
  getByType: async (type: ContentType): Promise<RecommendationItem[]> => {
    try {
      const response = await api.get<RecommendationItem[]>(`/catalog/${type}`);
      return response.data;
    } catch (error) {
      console.error("Error fetching catalog by type:", error);
      throw error;
    }
  },
};

export default api;