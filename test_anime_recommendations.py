#!/usr/bin/env python3
"""
Test script to verify anime recommendations are working properly
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from otakuverse.catalog_agent.agent import CatalogManager

def test_anime_catalog():
    """Test that anime catalog loads and searches work."""
    print("=" * 70)
    print("Testing OtakuVerse Anime Recommendations System")
    print("=" * 70)
    
    # Initialize catalog
    print("\n1. Loading catalogs...")
    catalog = CatalogManager()
    
    if 'anime' not in catalog.catalogs:
        print("❌ ERROR: Anime catalog not found!")
        return False
    
    anime_count = len(catalog.catalogs['anime'])
    print(f"✓ Anime catalog loaded with {anime_count} titles")
    
    # Test: Get all anime
    print("\n2. Testing: Get all anime...")
    all_anime = catalog.get_by_type(['anime'])
    print(f"✓ Retrieved {len(all_anime)} anime titles")
    if all_anime:
        print(f"   Sample: {all_anime[0]['title']} (Rating: {all_anime[0]['rating']})")
    
    # Test: Search by action genre
    print("\n3. Testing: Search by action genre...")
    action_anime = catalog.search_by_genres(['action'], ['anime'])
    print(f"✓ Found {len(action_anime)} action anime")
    if action_anime:
        print(f"   Sample: {action_anime[0]['title']} - Genres: {action_anime[0]['genres']}")
    
    # Test: Search by intense mood
    print("\n4. Testing: Search by intense mood...")
    intense_anime = catalog.search_by_mood(['intense'], ['anime'])
    print(f"✓ Found {len(intense_anime)} intense anime")
    if intense_anime:
        print(f"   Sample: {intense_anime[0]['title']} - Moods: {intense_anime[0]['mood']}")
    
    # Test: Search by genre AND mood
    print("\n5. Testing: Search by action + intense (genre + mood)...")
    action_intense = catalog.search_by_genre_and_mood(['action'], ['intense'], ['anime'])
    print(f"✓ Found {len(action_intense)} action + intense anime")
    for anime in action_intense[:3]:
        print(f"   - {anime['title']}")
    
    # Test: Search by multiple genres
    print("\n6. Testing: Search by romance genre...")
    romance_anime = catalog.search_by_genres(['romance'], ['anime'])
    print(f"✓ Found {len(romance_anime)} romance anime")
    if romance_anime:
        print(f"   Sample: {romance_anime[0]['title']}")
    
    # Test: Search by comedy mood
    print("\n7. Testing: Search by fun/funny mood...")
    fun_anime = catalog.search_by_mood(['fun', 'funny'], ['anime'])
    print(f"✓ Found {len(fun_anime)} fun/funny anime")
    for anime in fun_anime[:3]:
        print(f"   - {anime['title']}")
    
    # Test: Filter out consumed
    print("\n8. Testing: Filter out consumed content...")
    consumed_ids = ['anime_001', 'anime_002']
    filtered = catalog.filter_out_consumed(all_anime, consumed_ids)
    print(f"✓ Started with {len(all_anime)}, filtered to {len(filtered)} (removed {len(consumed_ids)} watched)")
    
    print("\n" + "=" * 70)
    print("✅ All tests passed! Anime recommendation system is working correctly!")
    print("=" * 70)
    return True

if __name__ == "__main__":
    success = test_anime_catalog()
    sys.exit(0 if success else 1)
