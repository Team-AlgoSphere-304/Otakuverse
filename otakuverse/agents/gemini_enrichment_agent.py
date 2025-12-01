"""
Gemini-Powered Agent for Entertainment Content Enrichment
Uses Gemini AI to generate recommendations and enriched data
"""

import os
import json
from typing import Optional, Dict, Any
import google.generativeai as genai


class GeminiEnrichmentAgent:
    """
    Agent that uses Gemini AI to enhance content data
    Reduces dependency on external APIs by leveraging LLM knowledge
    """
    
    def __init__(self):
        # Try both env var names
        self.api_key = os.getenv('GOOGLE_GENAI_API_KEY') or os.getenv('GOOGLE_API_KEY') or ''
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-2.0-flash')
        else:
            self.model = None
            print("[WARNING] Gemini API key not found. Agent will not enrich content.")
        
    async def get_content_enrichment(self, title: str, content_type: str) -> Dict[str, Any]:
        """
        Use Gemini to generate enriched content data including:
        - Estimated ratings
        - Genre information
        - Plot summary
        - Themes and mood
        - Similar recommendations
        
        This reduces API dependency by using Gemini's knowledge
        """
        
        if not self.model:
            return {
                "status": "unavailable",
                "message": "Gemini API not configured"
            }
        
        prompt = f"""
        Provide enriched data for the following entertainment content as JSON:
        
        Title: {title}
        Type: {content_type}
        
        Return a JSON object with:
        {{
            "title": "exact title",
            "content_type": "{content_type}",
            "estimated_rating": (0-10 scale based on your knowledge),
            "genres": ["genre1", "genre2"],
            "themes": ["theme1", "theme2"],
            "mood": ["mood1", "mood2"],
            "plot_summary": "brief 2-3 sentence summary",
            "why_watch": "compelling reason to watch this",
            "typical_audience": "who would enjoy this",
            "similar_titles": ["title1", "title2", "title3"]
        }}
        
        If you don't have specific information, provide your best estimate based on general knowledge.
        Return ONLY the JSON object, no additional text.
        """
        
        try:
            response = self.model.generate_content(prompt)
            
            # Parse JSON response
            response_text = response.text.strip()
            
            # Try to extract JSON if it's wrapped in markdown
            if response_text.startswith("```"):
                response_text = response_text.split("```")[1]
                if response_text.startswith("json"):
                    response_text = response_text[4:]
                response_text = response_text.strip()
            
            enriched_data = json.loads(response_text)
            
            return {
                "status": "success",
                "source": "gemini",
                "data": enriched_data
            }
            
        except json.JSONDecodeError as e:
            print(f"Error parsing Gemini response: {e}")
            return {
                "status": "error",
                "message": "Failed to parse enriched data"
            }
        except Exception as e:
            print(f"Error enriching content: {e}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    async def generate_personalized_recommendation(self,
                                                   title: str,
                                                   content_type: str,
                                                   user_genres: list[str],
                                                   user_moods: list[str]) -> str:
        """
        Generate a personalized recommendation explanation for why this content
        matches the user's preferences using Gemini
        """
        
        prompt = f"""
        Generate a compelling 2-3 sentence recommendation for this content:
        
        Content: {title} ({content_type})
        User Preferences:
        - Genres: {', '.join(user_genres)}
        - Moods: {', '.join(user_moods)}
        
        Explain specifically why this content is a great match for this user's taste.
        Be enthusiastic and specific. Return ONLY the recommendation text, nothing else.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"Error generating recommendation: {e}")
            return f"This {content_type} with {', '.join(user_genres)} genres matches your {', '.join(user_moods)} preference."
    
    async def search_catalog_with_ai(self,
                                     catalog_data: list[Dict],
                                     search_query: str,
                                     filters: Optional[Dict] = None) -> list[Dict]:
        """
        Use Gemini to intelligently search and rank catalog items
        based on semantic understanding of user query
        """
        
        # Prepare catalog summary for context
        catalog_summary = json.dumps(catalog_data[:20], indent=2)  # Top 20 items
        
        prompt = f"""
        Given this entertainment catalog:
        {catalog_summary}
        
        User search query: {search_query}
        
        Return a JSON array of recommended items from the catalog that best match the user's query.
        Rank them by relevance (best matches first).
        Return ONLY a JSON array of items, nothing else.
        
        Example format:
        [
            {{"id": "item_id", "title": "Title", "reason": "why it matches"}},
            ...
        ]
        """
        
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Extract JSON from markdown if needed
            if response_text.startswith("```"):
                response_text = response_text.split("```")[1]
                if response_text.startswith("json"):
                    response_text = response_text[4:]
                response_text = response_text.strip()
            
            recommendations = json.loads(response_text)
            return recommendations
            
        except Exception as e:
            print(f"Error in AI search: {e}")
            return []
    
    async def analyze_user_preferences(self, history: list[Dict]) -> Dict[str, Any]:
        """
        Use Gemini to analyze user's viewing history and infer preferences
        """
        
        history_summary = json.dumps(history[:10], indent=2)
        
        prompt = f"""
        Analyze this user's content history and infer their preferences:
        {history_summary}
        
        Return a JSON object with:
        {{
            "favorite_genres": ["genre1", "genre2"],
            "mood_preference": ["mood1", "mood2"],
            "content_type_preference": ["type1", "type2"],
            "inferred_taste": "description of their taste",
            "recommendation_strategy": "how to recommend for this user"
        }}
        
        Return ONLY the JSON object.
        """
        
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            if response_text.startswith("```"):
                response_text = response_text.split("```")[1]
                if response_text.startswith("json"):
                    response_text = response_text[4:]
                response_text = response_text.strip()
            
            preferences = json.loads(response_text)
            return preferences
            
        except Exception as e:
            print(f"Error analyzing preferences: {e}")
            return {
                "favorite_genres": [],
                "mood_preference": [],
                "content_type_preference": [],
                "inferred_taste": "Unable to analyze",
                "recommendation_strategy": "Start with popular titles"
            }


# Global instance
gemini_agent = GeminiEnrichmentAgent()
