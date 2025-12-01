export enum ContentType {
  ANIME = 'anime',
  MOVIES = 'movies',
  WEB_SERIES = 'web_series',
  MANGA = 'manga',
  MANHWA = 'manhwa',
  COMICS = 'comics',
  GAMES = 'games',
  LIGHT_NOVELS = 'light_novels',
  NOVELS = 'novels'
}

export enum Mood {
  HAPPY = 'happy',
  SAD = 'sad',
  EXCITED = 'excited',
  CALM = 'calm',
  MELANCHOLIC = 'melancholic',
  ADVENTUROUS = 'adventurous',
  NOSTALGIC = 'nostalgic',
  INTROSPECTIVE = 'introspective'
}

export enum StylePreference {
  DARK = 'dark',
  LIGHT = 'light',
  MATURE = 'mature',
  WHOLESOME = 'wholesome',
  EXPERIMENTAL = 'experimental',
  MAINSTREAM = 'mainstream'
}

export interface User {
  id: string;
  username: string;
  email: string;
  preferences?: {
    favorite_genres?: string[];
  };
}

export interface RecommendationItem {
  id: string;
  title: string;
  content_type: ContentType;
  genres: string[];
  description: string;
  explanation: string; // AI generated reason
  rating_score: number; // 0-10
  mal_score?: number; // MyAnimeList Score (0-10)
  imdb_score?: number; // IMDb Score (0-10)
  cover_image?: string;
  is_watched?: boolean;
  user_rating?: number;
}

export interface HistoryItem {
  id: string;
  item_id: string;
  title: string;
  content_type: ContentType;
  rating: number;
  watched_at: string;
}

export interface AuthResponse {
  token: string;
  user: User;
}

export interface RecommendationRequest {
  user_id: string;
  mood: Mood;
  genres: string[];
  content_types: ContentType[];
  preferred_style: StylePreference;
  custom_prompt?: string;
}

export interface RateRequest {
  user_id: string;
  item_id: string;
  rating: number;
}