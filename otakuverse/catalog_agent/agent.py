import json
import os
from pathlib import Path
# from google.adk.client import sdk  # Unused import - commented out
from typing import List, Dict, Optional


class CatalogManager:
    """Manage and search through content catalogs."""
    
    def __init__(self):
        self.catalogs = {}
        self.load_catalogs()
    
    def load_catalogs(self):
        """Load all catalog JSON files."""
        catalog_dir = Path(__file__).parent / "catalogs"
        
        catalog_files = [
            "anime.json", "movies.json", "web_series.json", 
            "manga.json", "manhwa.json", "comics.json", 
            "light_novels.json", "novels.json", "games.json"
        ]
        
        for catalog_file in catalog_files:
            file_path = catalog_dir / catalog_file
            if file_path.exists():
                with open(file_path, 'r') as f:
                    content_type = catalog_file.replace('.json', '')
                    self.catalogs[content_type] = json.load(f)
    
    def search_by_genres(self, genres: List[str], content_types: List[str] = None) -> List[Dict]:
        """Search for content matching given genres."""
        results = []
        
        catalogs_to_search = []
        if content_types:
            for ct in content_types:
                ct_key = ct.replace(' ', '_').lower()
                if ct_key in self.catalogs:
                    catalogs_to_search.append((ct_key, self.catalogs[ct_key]))
        else:
            catalogs_to_search = [(k, v) for k, v in self.catalogs.items()]
        
        if not catalogs_to_search:
            return results
        
        for content_type, catalog in catalogs_to_search:
            for item in catalog:
                item_genres = item.get('genres', [])
                if not item_genres:
                    continue
                    
                # Check if any of the user's genres match (case-insensitive)
                match = any(
                    any(genre.lower().strip() == g.lower().strip() for g in item_genres)
                    for genre in genres
                )
                
                if match:
                    item_copy = item.copy()
                    item_copy['content_type'] = content_type
                    results.append(item_copy)
        
        return sorted(results, key=lambda x: x.get('rating', 0), reverse=True)
    
    def search_by_mood(self, moods: List[str], content_types: List[str] = None) -> List[Dict]:
        """Search for content matching given moods."""
        results = []
        
        catalogs_to_search = []
        if content_types:
            for ct in content_types:
                ct_key = ct.replace(' ', '_').lower()
                if ct_key in self.catalogs:
                    catalogs_to_search.append((ct_key, self.catalogs[ct_key]))
        else:
            catalogs_to_search = [(k, v) for k, v in self.catalogs.items()]
        
        if not catalogs_to_search:
            return results
        
        for content_type, catalog in catalogs_to_search:
            for item in catalog:
                item_moods = item.get('mood', [])
                if not item_moods:
                    continue
                    
                # Check if any of the user's moods match (case-insensitive)
                match = any(
                    any(mood.lower().strip() == m.lower().strip() for m in item_moods)
                    for mood in moods
                )
                
                if match:
                    item_copy = item.copy()
                    item_copy['content_type'] = content_type
                    results.append(item_copy)
        
        return sorted(results, key=lambda x: x.get('rating', 0), reverse=True)
    
    def search_by_genre_and_mood(self, genres: List[str], moods: List[str], 
                                 content_types: List[str] = None) -> List[Dict]:
        """Search for content matching both genres and moods."""
        results = []
        
        catalogs_to_search = []
        if content_types:
            for ct in content_types:
                ct_key = ct.replace(' ', '_').lower()
                if ct_key in self.catalogs:
                    catalogs_to_search.append((ct_key, self.catalogs[ct_key]))
        else:
            catalogs_to_search = [(k, v) for k, v in self.catalogs.items()]
        
        if not catalogs_to_search:
            return results
        
        for content_type, catalog in catalogs_to_search:
            for item in catalog:
                item_genres = item.get('genres', [])
                item_moods = item.get('mood', [])
                
                if not item_genres or not item_moods:
                    continue
                
                # Check genre match
                genre_match = any(
                    any(genre.lower().strip() == g.lower().strip() for g in item_genres)
                    for genre in genres
                )
                
                # Check mood match
                mood_match = any(
                    any(mood.lower().strip() == m.lower().strip() for m in item_moods)
                    for mood in moods
                )
                
                if genre_match and mood_match:
                    item_copy = item.copy()
                    item_copy['content_type'] = content_type
                    results.append(item_copy)
        
        return sorted(results, key=lambda x: x.get('rating', 0), reverse=True)
    
    def get_by_type(self, content_types: List[str]) -> List[Dict]:
        """Get all content of specified types."""
        results = []
        
        for ct in content_types:
            ct_key = ct.replace(' ', '_').lower()
            if ct_key in self.catalogs:
                for item in self.catalogs[ct_key]:
                    item_copy = item.copy()
                    item_copy['content_type'] = ct_key
                    results.append(item_copy)
        
        return sorted(results, key=lambda x: x.get('rating', 0), reverse=True)
    
    def filter_out_consumed(self, content_list: List[Dict], consumed_ids: List[str]) -> List[Dict]:
        """Filter out content that user has already consumed."""
        return [item for item in content_list if item.get('id') not in consumed_ids]


# Global catalog manager instance
catalog_manager = CatalogManager()


def search_catalogs(genres: str = None, moods: str = None, content_types: str = None) -> dict:
    """Tool: Search catalogs for matching content."""
    try:
        genres_list = [g.strip() for g in genres.split(',')] if genres else []
        moods_list = [m.strip() for m in moods.split(',')] if moods else []
        types_list = [t.strip() for t in content_types.split(',')] if content_types else None
        
        if genres_list and moods_list:
            results = catalog_manager.search_by_genre_and_mood(genres_list, moods_list, types_list)
        elif genres_list:
            results = catalog_manager.search_by_genres(genres_list, types_list)
        elif moods_list:
            results = catalog_manager.search_by_mood(moods_list, types_list)
        elif types_list:
            results = catalog_manager.get_by_type(types_list)
        else:
            results = []
        
        return {
            "success": True,
            "count": len(results),
            "results": results[:20]  # Return top 20
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def get_available_types() -> dict:
    """Tool: Get all available content types."""
    types = list(catalog_manager.catalogs.keys())
    return {
        "success": True,
        "types": types
    }


def create_catalog_agent():
    """Create a catalog search agent."""
    try:
        from google.adk.client import sdk
        
        agent = sdk.Agent(
            model="models/gemini-2.5-flash",
            name="catalog_agent",
            description="Agent for searching and retrieving content from catalogs",
            tools=[
                sdk.Tool(
                    function_name="search_catalogs",
                    description="Search through all content catalogs by genres, moods, and content types",
                    parameters={
                        "genres": {"type": "string", "description": "Comma-separated genres to search"},
                        "moods": {"type": "string", "description": "Comma-separated moods to search"},
                        "content_types": {"type": "string", "description": "Comma-separated content types to filter"}
                    }
                ),
                sdk.Tool(
                    function_name="get_available_types",
                    description="Get list of all available content types in the catalog",
                    parameters={}
                )
            ]
        )
        return agent
    except ImportError:
        print("Warning: Google ADK SDK not available. create_catalog_agent() will not work.")
        print("Install google-adk to use this function: pip install google-adk")
        return None
