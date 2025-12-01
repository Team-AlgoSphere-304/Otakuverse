from google.adk.client import sdk
from .db import HistoryDatabase
from typing import Optional


def get_user_history(user_id: str, content_type: Optional[str] = None) -> dict:
    """Tool: Get user's content history."""
    db = HistoryDatabase()
    try:
        history = db.get_user_history(user_id, content_type)
        return {
            "success": True,
            "count": len(history),
            "history": history
        }
    finally:
        db.close()


def get_consumed_content_ids(user_id: str) -> dict:
    """Tool: Get IDs of all content consumed by user."""
    db = HistoryDatabase()
    try:
        consumed_ids = db.get_consumed_ids(user_id)
        return {
            "success": True,
            "consumed_count": len(consumed_ids),
            "content_ids": consumed_ids
        }
    finally:
        db.close()


def add_content_to_history(user_id: str, content_id: str, content_type: str, 
                           title: str, rating: Optional[float] = None, 
                           notes: str = "") -> dict:
    """Tool: Add content to user's history."""
    db = HistoryDatabase()
    try:
        db.add_to_history(user_id, content_id, content_type, title, rating, notes)
        return {
            "success": True,
            "message": f"Added '{title}' to {user_id}'s history"
        }
    finally:
        db.close()


def create_history_agent():
    """Create a history agent with tools."""
    agent = sdk.Agent(
        model="models/gemini-2.5-flash",
        name="history_agent",
        description="Agent for managing and retrieving user history and consumed content",
        tools=[
            sdk.Tool(
                function_name="get_user_history",
                description="Get user's complete content consumption history",
                parameters={
                    "user_id": {"type": "string", "description": "User ID"},
                    "content_type": {"type": "string", "description": "Optional content type filter"}
                }
            ),
            sdk.Tool(
                function_name="get_consumed_content_ids",
                description="Get IDs of all content consumed by user to avoid duplicates",
                parameters={
                    "user_id": {"type": "string", "description": "User ID"}
                }
            ),
            sdk.Tool(
                function_name="add_content_to_history",
                description="Add content to user's history after recommendation",
                parameters={
                    "user_id": {"type": "string", "description": "User ID"},
                    "content_id": {"type": "string", "description": "Content ID"},
                    "content_type": {"type": "string", "description": "Type of content"},
                    "title": {"type": "string", "description": "Content title"},
                    "rating": {"type": "number", "description": "Optional user rating"},
                    "notes": {"type": "string", "description": "Optional notes"}
                }
            )
        ]
    )
    return agent
