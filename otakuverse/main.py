#!/usr/bin/env python3
"""
OtakuVerse - Multi-agent Entertainment Recommendation System
Main CLI entry point for local development and testing
"""

import os
import sys
from datetime import datetime
from typing import List, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from orchestrator.agent import create_orchestrator_agent, create_recommendation_session
from mood_agent.agent import create_mood_agent
from history_agent.agent import create_history_agent
from history_agent.db import HistoryDatabase
from catalog_agent.agent import create_catalog_agent, CatalogManager
from ranking_agent.agent import create_ranking_agent


class OtakuVerseCLI:
    """CLI interface for OtakuVerse recommendation system."""
    
    def __init__(self):
        self.db = HistoryDatabase()
        self.catalog_manager = CatalogManager()
        self.current_user = None
        self.session = None
    
    def welcome(self):
        """Display welcome message."""
        print("\n" + "="*60)
        print("        🎌 Welcome to OtakuVerse 🎌")
        print("    Multi-Agent Entertainment Recommendation System")
        print("="*60 + "\n")
    
    def get_user_input(self, prompt: str) -> str:
        """Get user input."""
        return input(f"\n{prompt}: ").strip()
    
    def create_or_load_user(self):
        """Create new user or load existing user."""
        self.welcome()
        
        print("Do you have an existing OtakuVerse account?")
        print("1. Yes, use my existing ID")
        print("2. No, create a new account")
        
        choice = input("\nEnter your choice (1 or 2): ").strip()
        
        if choice == "1":
            user_id = self.get_user_input("Enter your user ID")
            user = self.db.get_user(user_id)
            if user:
                self.current_user = user_id
                print(f"\n✓ Welcome back, {user_id}!")
                return True
            else:
                print(f"✗ User ID '{user_id}' not found. Creating new account...")
                user_id = user_id
        else:
            user_id = self.get_user_input("Enter a new user ID (or press Enter for auto-generated)")
            if not user_id:
                user_id = f"user_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Create new user
        self.db.create_user(user_id)
        self.current_user = user_id
        print(f"\n✓ New account created! Your user ID: {user_id}")
        return True
    
    def show_content_types_menu(self) -> List[str]:
        """Show content types menu and let user select."""
        print("\n" + "-"*50)
        print("Available Content Types:")
        print("-"*50)
        
        types = [
            ("anime", "📺 Anime"),
            ("movies", "🎬 Movies"),
            ("web_series", "📱 Web Series"),
            ("manga", "📖 Manga"),
            ("manhwa", "🇰🇷 Manhwa"),
            ("comics", "💥 Comics"),
            ("light_novels", "📕 Light Novels"),
            ("novels", "📚 Novels"),
            ("games", "🎮 Games")
        ]
        
        print("\nSelect content types you want to explore:")
        print("(Enter numbers separated by commas, e.g., 1,3,5)")
        print()
        
        for i, (code, display) in enumerate(types, 1):
            print(f"{i}. {display}")
        
        while True:
            selection = input("\nYour selection: ").strip()
            try:
                indices = [int(x.strip()) - 1 for x in selection.split(',')]
                if all(0 <= i < len(types) for i in indices):
                    selected_types = [types[i][0] for i in indices]
                    print(f"\n✓ Selected: {', '.join([types[i][1] for i in indices])}")
                    return selected_types
                else:
                    print("✗ Invalid selection. Please try again.")
            except ValueError:
                print("✗ Invalid format. Please enter numbers separated by commas.")
    
    def get_preferences(self) -> dict:
        """Get user preferences for this session."""
        print("\n" + "="*50)
        print("Let's find the perfect entertainment for you!")
        print("="*50)
        
        # Get content types
        content_types = self.show_content_types_menu()
        
        # Get mood
        print("\n" + "-"*50)
        print("What's your current mood?")
        print("-"*50)
        print("Examples: happy, sad, relaxed, intense, thoughtful, funny, romantic, etc.")
        mood_input = self.get_user_input("Your mood")
        moods = [m.strip() for m in mood_input.split(',')] if mood_input else []
        
        # Get genres
        print("\n" + "-"*50)
        print("What genres interest you?")
        print("-"*50)
        print("Examples: action, romance, comedy, thriller, adventure, horror, sci-fi, fantasy, etc.")
        genre_input = self.get_user_input("Your preferred genres (comma-separated)")
        genres = [g.strip() for g in genre_input.split(',')] if genre_input else []
        
        # Get history
        history = self.db.get_user_history(self.current_user)
        consumed_ids = self.db.get_consumed_ids(self.current_user)
        
        return {
            "content_types": content_types,
            "moods": moods,
            "genres": genres,
            "history_count": len(history),
            "consumed_ids": consumed_ids
        }
    
    def get_recommendations(self, preferences: dict) -> List[dict]:
        """Get recommendations based on preferences."""
        print("\n" + "="*50)
        print("🔍 Searching for perfect recommendations...")
        print("="*50)
        
        try:
            # Search by genres and moods if available
            if preferences['genres'] and preferences['moods']:
                results = self.catalog_manager.search_by_genre_and_mood(
                    preferences['genres'],
                    preferences['moods'],
                    preferences['content_types']
                )
            elif preferences['genres']:
                results = self.catalog_manager.search_by_genres(
                    preferences['genres'],
                    preferences['content_types']
                )
            elif preferences['moods']:
                results = self.catalog_manager.search_by_mood(
                    preferences['moods'],
                    preferences['content_types']
                )
            else:
                results = self.catalog_manager.get_by_type(preferences['content_types'])
            
            # Filter out consumed content
            filtered = self.catalog_manager.filter_out_consumed(results, preferences['consumed_ids'])
            
            # Return top 10
            recommendations = filtered[:10]
            
            print(f"\n✓ Found {len(recommendations)} recommendations!")
            return recommendations
        
        except Exception as e:
            print(f"\n✗ Error finding recommendations: {e}")
            return []
    
    def display_recommendations(self, recommendations: List[dict]):
        """Display recommendations to user."""
        if not recommendations:
            print("\n✗ No recommendations found. Try different preferences!")
            return
        
        print("\n" + "="*70)
        print("YOUR RECOMMENDATIONS".center(70))
        print("="*70)
        
        for i, rec in enumerate(recommendations, 1):
            print(f"\n📌 RECOMMENDATION #{i}")
            print("-" * 70)
            print(f"Title:       {rec.get('title', 'N/A')}")
            print(f"Type:        {rec.get('content_type', 'N/A')}")
            print(f"Rating:      {'⭐' * int(rec.get('rating', 0))} ({rec.get('rating', 0)}/10)")
            print(f"Genres:      {', '.join(rec.get('genres', []))}")
            print(f"Mood:        {', '.join(rec.get('mood', []))}")
            print(f"Description: {rec.get('description', 'N/A')}")
        
        print("\n" + "="*70)
    
    def save_recommendations(self, recommendations: List[dict]):
        """Save recommendations to database."""
        batch_id = f"batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        for i, rec in enumerate(recommendations, 1):
            self.db.save_recommendation(
                self.current_user,
                batch_id,
                rec.get('id'),
                rec.get('content_type'),
                rec.get('title'),
                f"Matched genres: {', '.join(rec.get('genres', []))}",
                i
            )
        
        print(f"\n✓ Recommendations saved to your profile!")
    
    def run_session(self):
        """Run a complete recommendation session."""
        try:
            # Get user preferences
            preferences = self.get_preferences()
            
            # Get recommendations
            recommendations = self.get_recommendations(preferences)
            
            # Display recommendations
            self.display_recommendations(recommendations)
            
            # Save recommendations
            if recommendations:
                self.save_recommendations(recommendations)
                
                # Ask if user wants to mark any as consumed
                response = input("\n\nWould you like to add any of these to your history? (y/n): ").strip().lower()
                if response == 'y':
                    self.add_to_history(recommendations)
        
        except KeyboardInterrupt:
            print("\n\n✗ Session cancelled by user.")
        except Exception as e:
            print(f"\n✗ Error during session: {e}")
    
    def add_to_history(self, recommendations: List[dict]):
        """Let user add recommendations to history."""
        print("\nEnter the recommendation numbers you watched (comma-separated):")
        
        try:
            selection = input("Your selection: ").strip()
            indices = [int(x.strip()) - 1 for x in selection.split(',')]
            
            for i in indices:
                if 0 <= i < len(recommendations):
                    rec = recommendations[i]
                    
                    rating_input = input(f"\nRate '{rec.get('title')}' (1-10, or press Enter to skip): ").strip()
                    rating = None
                    if rating_input:
                        try:
                            rating = float(rating_input)
                        except ValueError:
                            pass
                    
                    notes = input("Any notes about this content? (optional): ").strip()
                    
                    self.db.add_to_history(
                        self.current_user,
                        rec.get('id'),
                        rec.get('content_type'),
                        rec.get('title'),
                        rating,
                        notes
                    )
                    
                    print(f"✓ Added '{rec.get('title')}' to your history!")
        
        except (ValueError, IndexError):
            print("✗ Invalid selection.")
    
    def view_history(self):
        """View user's content history."""
        history = self.db.get_user_history(self.current_user)
        
        if not history:
            print("\nYour history is empty!")
            return
        
        print("\n" + "="*70)
        print("YOUR CONTENT HISTORY".center(70))
        print("="*70)
        
        for i, item in enumerate(history, 1):
            print(f"\n{i}. {item.get('title', 'N/A')} ({item.get('content_type', 'N/A')})")
            if item.get('rating'):
                print(f"   Rating: {'⭐' * int(item.get('rating', 0))} ({item.get('rating')}/10)")
            if item.get('notes'):
                print(f"   Notes: {item.get('notes')}")
        
        print("\n" + "="*70)
    
    def main_menu(self):
        """Display main menu."""
        while True:
            print("\n" + "="*50)
            print("OtakuVerse Main Menu")
            print("="*50)
            print(f"User: {self.current_user}")
            print("\n1. Get Recommendations")
            print("2. View Your History")
            print("3. Exit")
            
            choice = input("\nEnter your choice (1-3): ").strip()
            
            if choice == "1":
                self.run_session()
            elif choice == "2":
                self.view_history()
            elif choice == "3":
                print("\n👋 Thank you for using OtakuVerse! See you next time!")
                break
            else:
                print("✗ Invalid choice. Please try again.")
    
    def run(self):
        """Run the CLI application."""
        try:
            if self.create_or_load_user():
                self.main_menu()
        except Exception as e:
            print(f"✗ Fatal error: {e}")
        finally:
            self.db.close()


def main():
    """Main entry point."""
    cli = OtakuVerseCLI()
    cli.run()


if __name__ == "__main__":
    main()
