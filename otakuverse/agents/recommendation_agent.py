"""
OtakuVerse Recommendation Agent using Google Generative AI
Follows the 5-Day AI Agents Intensive Course structure
"""

import os
import sys
import json
from typing import Any

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from catalog_agent.agent import CatalogManager


def search_catalog_by_genres(genres: list[str]) -> str:
    """Tool: Search catalog by genres"""
    try:
        results = catalog_manager.search_by_genres(genres)
        return json.dumps({
            "status": "success",
            "count": len(results),
            "items": results[:10]  # Return top 10
        })
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})


def search_catalog_by_mood(moods: list[str]) -> str:
    """Tool: Search catalog by mood"""
    try:
        results = catalog_manager.search_by_mood(moods)
        return json.dumps({
            "status": "success",
            "count": len(results),
            "items": results[:10]
        })
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})


def search_catalog_by_type(content_type: str) -> str:
    """Tool: Get all items of a specific content type"""
    try:
        results = catalog_manager.get_by_type(content_type)
        return json.dumps({
            "status": "success",
            "content_type": content_type,
            "count": len(results),
            "items": results[:10]
        })
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})


def get_enriched_item_data(title: str, content_type: str) -> str:
    """Tool: Fetch enriched item data with real ratings and images"""
    try:
        # This is an async function, but we'll run it synchronously
        import asyncio
        enriched = asyncio.run(
            image_rating_handler.get_enriched_item(title, content_type)
        )
        return json.dumps({
            "status": "success",
            "data": enriched
        })
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})


def register_agent_tools():
    """Register all tools with the ADK agent"""
    tools = [
        {
            "name": "search_catalog_by_genres",
            "description": "Search entertainment catalog by genres (action, comedy, drama, etc.)",
            "parameters": {
                "type": "object",
                "properties": {
                    "genres": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of genres to search for"
                    }
                },
                "required": ["genres"]
            },
            "function": search_catalog_by_genres
        },
        {
            "name": "search_catalog_by_mood",
            "description": "Search entertainment catalog by mood (relaxing, intense, thought-provoking, etc.)",
            "parameters": {
                "type": "object",
                "properties": {
                    "moods": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of moods to search for"
                    }
                },
                "required": ["moods"]
            },
            "function": search_catalog_by_mood
        },
        {
            "name": "search_catalog_by_type",
            "description": "Get all items of a specific entertainment type (anime, manga, movies, web_series, etc.)",
            "parameters": {
                "type": "object",
                "properties": {
                    "content_type": {
                        "type": "string",
                        "description": "Type of entertainment content"
                    }
                },
                "required": ["content_type"]
            },
            "function": search_catalog_by_type
        },
        {
            "name": "get_enriched_item_data",
            "description": "Get enriched data for an item including MAL/IMDb ratings and cover images",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "Title of the entertainment item"
                    },
                    "content_type": {
                        "type": "string",
                        "description": "Type of content (anime, manga, movie, etc.)"
                    }
                },
                "required": ["title", "content_type"]
            },
            "function": get_enriched_item_data
        }
    ]
    return tools


class OtakuVerseRecommendationAgent:
    """
    AI Agent for personalized entertainment recommendations
    Uses Agent Development Kit and Gemini API
    """
    
    def __init__(self):
        self.gemini_api_key = os.getenv('GOOGLE_GENAI_API_KEY', '')
        self.model = "gemini-2.5-flash"
        self.tools = register_agent_tools()
        
    async def get_recommendations(self, 
                                 user_preferences: dict,
                                 genres: list[str] = None,
                                 moods: list[str] = None,
                                 content_types: list[str] = None) -> dict:
        """
        Main agent method to generate personalized recommendations
        
        Args:
            user_preferences: User profile and preferences
            genres: Preferred genres
            moods: Preferred moods
            content_types: Preferred content types
            
        Returns:
            Recommendations with explanations
        """
        
        # Build the user context
        user_context = f"""
        User Preferences:
        - Genres: {', '.join(genres) if genres else 'Any'}
        - Moods: {', '.join(moods) if moods else 'Any'}
        - Content Types: {', '.join(content_types) if content_types else 'Any'}
        """
        
        prompt = f"""
        You are OtakuVerse, an intelligent entertainment recommendation agent powered by AI.
        
        {user_context}
        
        Based on the user's preferences, help them discover entertainment content they will love.
        
        Steps:
        1. Use the available tools to search for content matching their preferences
        2. For each promising result, fetch enriched data with real ratings and images
        3. Provide 5-10 personalized recommendations with detailed explanations of why each is a good match
        4. Include ratings from MAL (MyAnimeList) or IMDb when available
        
        Be conversational, enthusiastic, and specific about why each recommendation matches their taste.
        """
        
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.gemini_api_key)
            
            # Create the agent request with tools
            response = await self._call_agent_with_tools(prompt)
            
            return {
                "status": "success",
                "recommendations": response,
                "user_context": user_preferences
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
    
    async def _call_agent_with_tools(self, prompt: str) -> str:
        """Call Gemini with tool integration"""
        import google.generativeai as genai
        
        # Tool definitions for Gemini
        tools_for_gemini = [
            {
                "type": "function",
                "function": {
                    "name": "search_catalog_by_genres",
                    "description": "Search entertainment catalog by genres",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "genres": {
                                "type": "array",
                                "items": {"type": "string"}
                            }
                        },
                        "required": ["genres"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "search_catalog_by_mood",
                    "description": "Search entertainment catalog by mood",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "moods": {
                                "type": "array",
                                "items": {"type": "string"}
                            }
                        },
                        "required": ["moods"]
                    }
                }
            }
        ]
        
        model = genai.GenerativeModel(
            self.model,
            tools=tools_for_gemini
        )
        
        chat = model.start_chat()
        response = chat.send_message(prompt)
        
        # Process tool calls if any
        while response.candidates[0].content.parts:
            part = response.candidates[0].content.parts[0]
            
            if hasattr(part, 'function_call'):
                # Handle tool call
                func_call = part.function_call
                func_name = func_call.name
                
                # Map function names to actual functions
                tool_responses = {
                    "search_catalog_by_genres": lambda args: search_catalog_by_genres(args['genres']),
                    "search_catalog_by_mood": lambda args: search_catalog_by_mood(args['moods']),
                }
                
                if func_name in tool_responses:
                    result = tool_responses[func_name](func_call.args)
                    
                    # Continue conversation with tool result
                    response = chat.send_message(
                        [
                            {
                                "type": "function_result",
                                "function_call_id": func_name,
                                "result": result
                            }
                        ]
                    )
            else:
                break
        
        return response.text


# Export the agent
agent = OtakuVerseRecommendationAgent()
