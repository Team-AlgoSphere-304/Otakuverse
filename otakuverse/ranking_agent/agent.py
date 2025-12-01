from google.adk.client import sdk


def rank_recommendations(recommendations: str, user_preferences: str) -> dict:
    """Rank recommendations based on user preferences."""
    return {
        "ranked": True,
        "recommendations": recommendations
    }


def create_ranking_agent():
    """Create a ranking agent for ordering recommendations."""
    agent = sdk.Agent(
        model="models/gemini-2.5-flash",
        name="ranking_agent",
        description="Agent for ranking recommendations and providing personalized explanations",
        system_prompt="""You are a recommendation ranking specialist for OtakuVerse.
Your job is to:
1. Rank recommendations from best to least suitable for the user
2. Provide personalized explanations for each recommendation
3. Consider the user's mood, genres, content preferences, and history
4. Give compelling reasons why each recommendation matches their request

Format explanations to be engaging and encourage users to try the content."""
    )
    return agent
