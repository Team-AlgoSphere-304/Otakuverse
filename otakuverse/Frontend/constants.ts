import { ContentType, Mood, StylePreference } from './types';

export const GENRES = [
  'Action', 'Adventure', 'Comedy', 'Drama', 'Ecchi', 'Fantasy', 
  'Horror', 'Mahou Shoujo', 'Mecha', 'Music', 'Mystery', 'Psychological', 
  'Romance', 'Sci-Fi', 'Slice of Life', 'Sports', 'Supernatural', 'Thriller', 
  'Isekai', 'Cyberpunk', 'Steampunk'
];

export const CONTENT_TYPE_LABELS: Record<ContentType, string> = {
  [ContentType.ANIME]: 'Anime',
  [ContentType.MOVIES]: 'Movies',
  [ContentType.WEB_SERIES]: 'Web Series',
  [ContentType.MANGA]: 'Manga',
  [ContentType.MANHWA]: 'Manhwa',
  [ContentType.COMICS]: 'Comics',
  [ContentType.GAMES]: 'Games',
  [ContentType.LIGHT_NOVELS]: 'Light Novels',
  [ContentType.NOVELS]: 'Novels',
};

export const MOOD_LABELS: Record<Mood, string> = {
  [Mood.HAPPY]: 'Happy 😊',
  [Mood.SAD]: 'Sad 😢',
  [Mood.EXCITED]: 'Excited 🤩',
  [Mood.CALM]: 'Calm 😌',
  [Mood.MELANCHOLIC]: 'Melancholic 🌧️',
  [Mood.ADVENTUROUS]: 'Adventurous ⚔️',
  [Mood.NOSTALGIC]: 'Nostalgic 🕰️',
  [Mood.INTROSPECTIVE]: 'Introspective 🤔',
};

export const STYLE_LABELS: Record<StylePreference, string> = {
  [StylePreference.DARK]: 'Dark 🌑',
  [StylePreference.LIGHT]: 'Light ☀️',
  [StylePreference.MATURE]: 'Mature 🍷',
  [StylePreference.WHOLESOME]: 'Wholesome 💖',
  [StylePreference.EXPERIMENTAL]: 'Experimental 🧪',
  [StylePreference.MAINSTREAM]: 'Mainstream 🍿',
};
