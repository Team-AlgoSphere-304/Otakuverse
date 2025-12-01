from google.adk.client import sdk


def extract_mood_and_preferences(user_input: str) -> dict:
    """Extract mood, genres, and preferences from user input."""
    # This function will be called by the agent
    # The actual extraction is handled by Gemini through the agent
    return {
        "raw_input": user_input,
        "extracted": True
    }


def create_mood_agent():
    """Create a mood extraction agent."""
    agent = sdk.Agent(
        model="models/gemini-2.5-flash",
        name="mood_agent",
        description="Agent for extracting user mood, preferences, genres, and desired content types",
        system_prompt="""You are a mood and preference extraction specialist for the OtakuVerse recommendation system.
Your job is to:
1. Analyze user input to determine their current mood
2. Extract preferred genres and styles
3. Understand which content types they're interested in (anime, movies, web series, manga, manhwa, comics, light novels, novels, games)
4. Identify any specific preferences or constraints

Always be conversational and help users articulate what they're looking for.
Return your analysis in a clear, structured format."""
    )
    return agent
