import React, { useState, useEffect } from 'react';
import { AlertCircle } from 'lucide-react';

interface OptimizedImageProps {
  src?: string | null;
  alt: string;
  title: string;
  className?: string;
  fallbackEmoji?: string;
}

/**
 * Ultra-fast image loading with fallback to Gemini-generated placeholder
 */
const OptimizedImage: React.FC<OptimizedImageProps> = ({
  src,
  alt,
  title,
  className = "w-full h-full object-cover",
  fallbackEmoji = "🎬"
}) => {
  const [imageLoaded, setImageLoaded] = useState(false);
  const [imageFailed, setImageFailed] = useState(false);
  const [imageUrl, setImageUrl] = useState<string | null>(src || null);

  useEffect(() => {
    setImageUrl(src || null);
    setImageLoaded(false);
    setImageFailed(false);
  }, [src]);

  const handleImageLoad = () => {
    setImageLoaded(true);
    setImageFailed(false);
  };

  const handleImageError = () => {
    console.warn(`Failed to load image: ${src}`);
    setImageFailed(true);
    setImageLoaded(false);
  };

  // Generate emoji-based placeholder based on content type
  const getPlaceholderEmoji = () => {
    if (title.toLowerCase().includes('anime')) return '🎌';
    if (title.toLowerCase().includes('manga')) return '📚';
    if (title.toLowerCase().includes('game')) return '🎮';
    if (title.toLowerCase().includes('movie')) return '🎬';
    if (title.toLowerCase().includes('series')) return '📺';
    return fallbackEmoji;
  };

  // If no image available or failed, show emoji placeholder
  if (!imageUrl || imageFailed) {
    return (
      <div
        className={`${className} bg-gradient-to-br from-slate-700 to-slate-900 flex items-center justify-center`}
        title={title}
      >
        <div className="text-center">
          <div className="text-5xl mb-2">{getPlaceholderEmoji()}</div>
          <div className="text-xs text-slate-400 px-2">{title}</div>
        </div>
      </div>
    );
  }

  return (
    <>
      {/* Loading skeleton */}
      {!imageLoaded && (
        <div
          className={`${className} bg-slate-700 animate-pulse flex items-center justify-center`}
        >
          <div className="text-3xl opacity-50">{getPlaceholderEmoji()}</div>
        </div>
      )}

      {/* Actual image */}
      <img
        src={imageUrl}
        alt={alt}
        title={title}
        className={`${className} ${imageLoaded ? 'opacity-100' : 'opacity-0'} transition-opacity duration-300`}
        onLoad={handleImageLoad}
        onError={handleImageError}
        loading="lazy"
      />
    </>
  );
};

export default OptimizedImage;
