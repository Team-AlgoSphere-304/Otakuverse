interface ImageData {
  posterUrl: string;
  bannerUrl: string;
  thumbnailUrl: string;
  coverUrl: string;
}

interface RatingData {
  imdbRating?: number;
  malRating?: number;
  userRating?: number;
  ratingCount?: number;
  source?: string;
}

class ImageAndRatingService {
  private imdbCache = new Map<string, ImageData>();
  private ratingCache = new Map<string, RatingData>();

  // Get images from IMDb via OMDb API
  async getImdbImages(title: string, year?: number): Promise<ImageData | null> {
    const cacheKey = `${title}-${year || 'unknown'}`;
    
    if (this.imdbCache.has(cacheKey)) {
      return this.imdbCache.get(cacheKey) || null;
    }

    try {
      const omdbApiKey = (import.meta as any).env?.VITE_OMDB_API_KEY;
      if (!omdbApiKey) {
        console.warn('OMDB API key not configured');
        return null;
      }

      const omdbUrl = `https://www.omdbapi.com/?apikey=${omdbApiKey}&t=${encodeURIComponent(title)}&y=${year || ''}`;
      const response = await fetch(omdbUrl);
      const data = await response.json();

      if (data.Poster && data.Poster !== 'N/A') {
        const imageData: ImageData = {
          posterUrl: data.Poster,
          bannerUrl: data.Poster,
          thumbnailUrl: data.Poster,
          coverUrl: data.Poster,
        };
        this.imdbCache.set(cacheKey, imageData);
        return imageData;
      }
      return null;
    } catch (error) {
      console.error('Error fetching IMDb images:', error);
      return null;
    }
  }

  // Get images from MyAnimeList via Jikan API
  async getMalImages(title: string, type: 'anime' | 'manga'): Promise<ImageData | null> {
    const cacheKey = `mal-${type}-${title}`;
    
    if (this.imdbCache.has(cacheKey)) {
      return this.imdbCache.get(cacheKey) || null;
    }

    try {
      const jikanUrl = `https://api.jikan.moe/v4/search/${type}?query=${encodeURIComponent(title)}&limit=1`;
      const response = await fetch(jikanUrl);
      const data = await response.json();

      if (data.data && data.data.length > 0) {
        const result = data.data[0];
        const imageData: ImageData = {
          posterUrl: result.images?.jpg?.image_url || result.images?.jpg?.small_image_url || '',
          bannerUrl: result.images?.jpg?.large_image_url || '',
          thumbnailUrl: result.images?.jpg?.small_image_url || '',
          coverUrl: result.images?.jpg?.image_url || '',
        };
        this.imdbCache.set(cacheKey, imageData);
        return imageData;
      }
      return null;
    } catch (error) {
      console.error('Error fetching MAL images:', error);
      return null;
    }
  }

  // Get ratings from multiple sources
  async getRatings(title: string, type: string): Promise<RatingData | null> {
    const cacheKey = `${title}-${type}`;
    
    if (this.ratingCache.has(cacheKey)) {
      return this.ratingCache.get(cacheKey) || null;
    }

    const ratingData: RatingData = {};

    try {
      // Try IMDb via OMDb for movies and series
      if (type === 'movies' || type === 'web_series') {
        const omdbApiKey = (import.meta as any).env?.VITE_OMDB_API_KEY;
        if (omdbApiKey) {
          const omdbUrl = `https://www.omdbapi.com/?apikey=${omdbApiKey}&t=${encodeURIComponent(title)}`;
          const omdbResponse = await fetch(omdbUrl);
          const omdbData = await omdbResponse.json();
          if (omdbData.imdbRating && omdbData.imdbRating !== 'N/A') {
            ratingData.imdbRating = parseFloat(omdbData.imdbRating);
          }
        }
      }

      // Try MyAnimeList for anime/manga
      if (type === 'anime' || type === 'manga' || type === 'light_novels') {
        const searchType = type === 'light_novels' ? 'manga' : type;
        const jikanUrl = `https://api.jikan.moe/v4/search/${searchType}?query=${encodeURIComponent(title)}&limit=1`;
        const malResponse = await fetch(jikanUrl);
        const malData = await malResponse.json();
        if (malData.data && malData.data.length > 0) {
          ratingData.malRating = malData.data[0].score || undefined;
          ratingData.ratingCount = malData.data[0].scored_by || undefined;
        }
      }

      ratingData.source = Object.keys(ratingData).join(', ');
      this.ratingCache.set(cacheKey, ratingData);
      return ratingData;
    } catch (error) {
      console.error('Error fetching ratings:', error);
      return null;
    }
  }

  // Get fallback images
  getFallbackImage(contentType: string): string {
    const fallbacks: Record<string, string> = {
      anime: 'https://via.placeholder.com/300x400?text=Anime',
      movies: 'https://via.placeholder.com/300x400?text=Movie',
      manga: 'https://via.placeholder.com/300x400?text=Manga',
      games: 'https://via.placeholder.com/300x400?text=Game',
      web_series: 'https://via.placeholder.com/300x400?text=Web+Series',
      comics: 'https://via.placeholder.com/300x400?text=Comic',
      novels: 'https://via.placeholder.com/300x400?text=Novel',
      light_novels: 'https://via.placeholder.com/300x400?text=Light+Novel',
      manhwa: 'https://via.placeholder.com/300x400?text=Manhwa',
    };
    return fallbacks[contentType] || fallbacks.anime;
  }

  clearCache() {
    this.imdbCache.clear();
    this.ratingCache.clear();
  }
}

export default new ImageAndRatingService();
