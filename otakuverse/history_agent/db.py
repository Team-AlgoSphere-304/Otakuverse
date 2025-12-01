import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional


class HistoryDatabase:
    """SQLite database wrapper for managing user history and preferences."""
    
    def __init__(self, db_path: str = "otakuverse.db"):
        """Initialize the database connection and create tables if needed."""
        self.db_path = db_path
        self.connection = None
        self.init_db()
    
    def init_db(self):
        """Create tables if they don't exist."""
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row
        cursor = self.connection.cursor()
        
        # User table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                preferences JSON
            )
        """)
        
        # Content history table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS content_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                content_id TEXT NOT NULL,
                content_type TEXT NOT NULL,
                title TEXT NOT NULL,
                consumed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                rating REAL,
                notes TEXT,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)
        
        # Recommendations table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS recommendations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                recommendation_batch_id TEXT NOT NULL,
                content_id TEXT NOT NULL,
                content_type TEXT NOT NULL,
                title TEXT NOT NULL,
                explanation TEXT,
                ranking INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                viewed BOOLEAN DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)
        
        self.connection.commit()
    
    def create_user(self, user_id: str, preferences: Optional[Dict] = None):
        """Create a new user."""
        cursor = self.connection.cursor()
        prefs_json = json.dumps(preferences) if preferences else json.dumps({})
        
        cursor.execute("""
            INSERT OR REPLACE INTO users (user_id, preferences)
            VALUES (?, ?)
        """, (user_id, prefs_json))
        
        self.connection.commit()
    
    def get_user(self, user_id: str) -> Optional[Dict]:
        """Get user by ID."""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        
        if row:
            return dict(row)
        return None
    
    def add_to_history(self, user_id: str, content_id: str, content_type: str, 
                       title: str, rating: Optional[float] = None, notes: str = ""):
        """Add content to user's history."""
        cursor = self.connection.cursor()
        
        cursor.execute("""
            INSERT INTO content_history 
            (user_id, content_id, content_type, title, rating, notes)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, content_id, content_type, title, rating, notes))
        
        self.connection.commit()
    
    def get_user_history(self, user_id: str, content_type: Optional[str] = None) -> List[Dict]:
        """Get user's content history, optionally filtered by type."""
        cursor = self.connection.cursor()
        
        if content_type:
            cursor.execute("""
                SELECT * FROM content_history 
                WHERE user_id = ? AND content_type = ?
                ORDER BY consumed_at DESC
            """, (user_id, content_type))
        else:
            cursor.execute("""
                SELECT * FROM content_history 
                WHERE user_id = ?
                ORDER BY consumed_at DESC
            """, (user_id,))
        
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    
    def get_consumed_ids(self, user_id: str) -> List[str]:
        """Get all content IDs that a user has consumed."""
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT DISTINCT content_id FROM content_history 
            WHERE user_id = ?
        """, (user_id,))
        
        rows = cursor.fetchall()
        return [row[0] for row in rows]
    
    def save_recommendation(self, user_id: str, batch_id: str, content_id: str,
                           content_type: str, title: str, explanation: str, ranking: int):
        """Save a recommendation for the user."""
        cursor = self.connection.cursor()
        
        cursor.execute("""
            INSERT INTO recommendations 
            (user_id, recommendation_batch_id, content_id, content_type, title, explanation, ranking)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (user_id, batch_id, content_id, content_type, title, explanation, ranking))
        
        self.connection.commit()
    
    def get_recommendations(self, user_id: str, batch_id: Optional[str] = None) -> List[Dict]:
        """Get recommendations for a user."""
        cursor = self.connection.cursor()
        
        if batch_id:
            cursor.execute("""
                SELECT * FROM recommendations 
                WHERE user_id = ? AND recommendation_batch_id = ?
                ORDER BY ranking ASC
            """, (user_id, batch_id))
        else:
            cursor.execute("""
                SELECT * FROM recommendations 
                WHERE user_id = ?
                ORDER BY created_at DESC, ranking ASC
            """, (user_id,))
        
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    
    def update_preferences(self, user_id: str, preferences: Dict):
        """Update user preferences."""
        cursor = self.connection.cursor()
        prefs_json = json.dumps(preferences)
        
        cursor.execute("""
            UPDATE users 
            SET preferences = ?, updated_at = CURRENT_TIMESTAMP
            WHERE user_id = ?
        """, (prefs_json, user_id))
        
        self.connection.commit()
    
    def close(self):
        """Close the database connection."""
        if self.connection:
            self.connection.close()
    
    def __del__(self):
        """Ensure connection is closed when object is destroyed."""
        self.close()
