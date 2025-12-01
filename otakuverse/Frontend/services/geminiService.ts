interface GeminiResponse {
  explanation: string;
  summary: string;
  matchPercentage: number;
  keyReasons: string[];
}

class GeminiService {
  private apiKey = import.meta.env.VITE_GEMINI_API_KEY;
  private apiUrl = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent';

  async extractRealData(itemTitle: string, itemType: string): Promise<any> {
    try {
      const prompt = `Search for and provide real, accurate information about the ${itemType} titled "${itemTitle}":
        - Official plot/description
        - Release date
        - Creator/Director/Author
        - Main genres
        - Age rating
        - Current ratings from major platforms
        - Notable awards or accolades
        Return as JSON format with these exact keys: plot, releaseDate, creator, genres, ageRating, ratings, awards`;

      const response = await fetch(
        `${this.apiUrl}?key=${this.apiKey}`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            contents: [
              {
                parts: [
                  {
                    text: prompt,
                  },
                ],
              },
            ],
            generationConfig: {
              temperature: 0.7,
              topK: 40,
              topP: 0.95,
              maxOutputTokens: 2048,
            },
          }),
        }
      );

      const data = await response.json();
      if (data.candidates && data.candidates[0]?.content?.parts[0]?.text) {
        const text = data.candidates[0].content.parts[0].text;
        const jsonMatch = text.match(/\{[\s\S]*\}/);
        if (jsonMatch) {
          return JSON.parse(jsonMatch[0]);
        }
      }
      return null;
    } catch (error) {
      console.error('Error extracting data from Gemini:', error);
      return null;
    }
  }

  async generateRecommendationExplanation(
    itemTitle: string,
    itemType: string,
    mood: string,
    genres: string[],
    userPreferences: string
  ): Promise<GeminiResponse> {
    try {
      const prompt = `You are an entertainment recommendation expert. Explain why the ${itemType} "${itemTitle}" 
        is a perfect match for a user with these preferences:
        
        Mood: ${mood}
        Genres they like: ${genres.join(', ')}
        User preferences: ${userPreferences}
        
        Provide a JSON response with exactly these keys:
        - explanation: A brief 2-3 sentence explanation
        - summary: A one-line summary
        - matchPercentage: A number 0-100
        - keyReasons: An array of exactly 3 key reasons as strings
        
        Return ONLY valid JSON, no other text.`;

      const response = await fetch(
        `${this.apiUrl}?key=${this.apiKey}`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            contents: [
              {
                parts: [
                  {
                    text: prompt,
                  },
                ],
              },
            ],
            generationConfig: {
              temperature: 0.8,
              topK: 40,
              topP: 0.95,
              maxOutputTokens: 1024,
            },
          }),
        }
      );

      const data = await response.json();
      if (data.candidates && data.candidates[0]?.content?.parts[0]?.text) {
        const text = data.candidates[0].content.parts[0].text;
        const jsonMatch = text.match(/\{[\s\S]*\}/);
        if (jsonMatch) {
          const parsed = JSON.parse(jsonMatch[0]);
          return {
            explanation: parsed.explanation || 'Perfect match for your taste!',
            summary: parsed.summary || 'Highly recommended',
            matchPercentage: parsed.matchPercentage || 75,
            keyReasons: parsed.keyReasons || ['Great pick', 'Well-aligned', "You'll love it"],
          };
        }
      }
      return {
        explanation: 'Perfect match for your taste!',
        summary: 'Highly recommended',
        matchPercentage: 75,
        keyReasons: ['Great pick', 'Well-aligned', "You'll love it"],
      };
    } catch (error) {
      console.error('Error generating explanation:', error);
      return {
        explanation: 'A great recommendation for you',
        summary: 'Well-matched',
        matchPercentage: 70,
        keyReasons: ['Matches preferences', 'Quality content', 'Popular choice'],
      };
    }
  }

  async generateCatalogDescription(title: string, type: string): Promise<string> {
    try {
      const prompt = `Write a short, engaging description (2-3 sentences) for the ${type} "${title}". 
        Make it appealing to potential viewers/readers. Be factual and engaging. Return only the description, no JSON.`;

      const response = await fetch(
        `${this.apiUrl}?key=${this.apiKey}`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            contents: [
              {
                parts: [
                  {
                    text: prompt,
                  },
                ],
              },
            ],
            generationConfig: {
              temperature: 0.7,
              maxOutputTokens: 256,
            },
          }),
        }
      );

      const data = await response.json();
      if (data.candidates && data.candidates[0]?.content?.parts[0]?.text) {
        return data.candidates[0].content.parts[0].text;
      }
      return 'Check this out!';
    } catch (error) {
      console.error('Error generating description:', error);
      return 'A great piece of entertainment';
    }
  }
}

export default new GeminiService();
