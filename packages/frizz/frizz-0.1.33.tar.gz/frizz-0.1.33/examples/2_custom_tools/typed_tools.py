"""
Example 2: Defining Custom Tools with Typed Parameters and Validation

This example demonstrates how to create complex tools with proper type validation
using Pydantic models, including nested models and validation constraints.
"""
import asyncio
import os
import sys
from datetime import datetime
from enum import Enum

from aikernel import (
    Conversation,
    LLMMessagePart,
    LLMSystemMessage,
    LLMUserMessage,
    get_router,
)
from pydantic import BaseModel, Field, field_validator

# Add the parent directory to the path so we can import the custom_agent module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from custom_agent import Agent

from frizz import tool


# Define complex parameter models with validation
class Genre(str, Enum):
    """Valid music genres for the recommendation tool."""
    POP = "pop"
    ROCK = "rock"
    JAZZ = "jazz"
    CLASSICAL = "classical"
    ELECTRONIC = "electronic"
    HIP_HOP = "hip_hop"


class MoodTag(str, Enum):
    """Mood tags for music recommendations."""
    HAPPY = "happy"
    SAD = "sad"
    ENERGETIC = "energetic"
    RELAXED = "relaxed"
    FOCUSED = "focused"


class RecommendationParams(BaseModel):
    """Parameters for the music recommendation tool with validation."""
    genres: list[Genre] = Field(..., description="List of music genres to include")
    release_year_min: int | None = Field(None, description="Minimum release year")
    release_year_max: int | None = Field(None, description="Maximum release year")
    mood: MoodTag | None = Field(None, description="Desired mood")
    limit: int = Field(5, description="Number of recommendations to return", ge=1, le=10)
    
    @field_validator("release_year_min", "release_year_max")
    def validate_year(cls, v):
        if v is not None:
            current_year = datetime.now().year
            if v < 1900 or v > current_year:
                raise ValueError(f"Year must be between 1900 and {current_year}")
        return v
    
    @field_validator("release_year_max")
    def validate_year_range(cls, v, info):
        if v is not None and info.data.get("release_year_min") is not None:
            if v < info.data["release_year_min"]:
                raise ValueError("Maximum year cannot be less than minimum year")
        return v


class Song(BaseModel):
    """Representation of a song recommendation."""
    title: str
    artist: str
    release_year: int
    genre: Genre
    mood: MoodTag


class RecommendationResult(BaseModel):
    """Return type for the music recommendation tool."""
    recommendations: list[Song]
    count: int
    genres_included: list[Genre]
    message: str


# Simple context for this example
class MusicServiceContext:
    """Context for the music service with mock data."""
    def __init__(self):
        # Mock database of songs
        self.song_database = [
            Song(title="Bohemian Rhapsody", artist="Queen", release_year=1975, genre=Genre.ROCK, mood=MoodTag.ENERGETIC),
            Song(title="Billie Jean", artist="Michael Jackson", release_year=1983, genre=Genre.POP, mood=MoodTag.ENERGETIC),
            Song(title="Take Five", artist="Dave Brubeck", release_year=1959, genre=Genre.JAZZ, mood=MoodTag.RELAXED),
            Song(title="Moonlight Sonata", artist="Beethoven", release_year=1801, genre=Genre.CLASSICAL, mood=MoodTag.SAD),
            Song(title="Strobe", artist="Deadmau5", release_year=2010, genre=Genre.ELECTRONIC, mood=MoodTag.FOCUSED),
            Song(title="Juicy", artist="The Notorious B.I.G.", release_year=1994, genre=Genre.HIP_HOP, mood=MoodTag.HAPPY),
            Song(title="Yesterday", artist="The Beatles", release_year=1965, genre=Genre.ROCK, mood=MoodTag.SAD),
            Song(title="La Vie En Rose", artist="Edith Piaf", release_year=1945, genre=Genre.JAZZ, mood=MoodTag.RELAXED),
            Song(title="Blinding Lights", artist="The Weeknd", release_year=2019, genre=Genre.POP, mood=MoodTag.ENERGETIC),
            Song(title="Gymnopédie No.1", artist="Erik Satie", release_year=1888, genre=Genre.CLASSICAL, mood=MoodTag.RELAXED),
        ]


@tool(name="recommend_music")
async def recommend_music(
    *, context: MusicServiceContext, parameters: RecommendationParams, conversation: Conversation
) -> RecommendationResult:
    """Recommend songs based on genres, release years, and mood."""
    # Get all songs from our mock database
    all_songs = context.song_database
    
    # Filter based on parameters
    filtered_songs = all_songs
    
    # Filter by genres
    if parameters.genres:
        filtered_songs = [s for s in filtered_songs if s.genre in parameters.genres]
    
    # Filter by release year min
    if parameters.release_year_min is not None:
        filtered_songs = [s for s in filtered_songs if s.release_year >= parameters.release_year_min]
    
    # Filter by release year max
    if parameters.release_year_max is not None:
        filtered_songs = [s for s in filtered_songs if s.release_year <= parameters.release_year_max]
    
    # Filter by mood
    if parameters.mood is not None:
        filtered_songs = [s for s in filtered_songs if s.mood == parameters.mood]
    
    # Limit results
    limited_songs = filtered_songs[:parameters.limit]
    
    # Get genres included in results
    genres_included = list(set(song.genre for song in limited_songs))
    
    return RecommendationResult(
        recommendations=limited_songs,
        count=len(limited_songs),
        genres_included=genres_included,
        message=f"Found {len(limited_songs)} songs matching your criteria."
    )


async def main():
    # Create the context and agent
    context = MusicServiceContext()
    
    agent = Agent(
        tools=[recommend_music],
        context=context,
        system_message=LLMSystemMessage(parts=[LLMMessagePart(content="""
            You are a music recommendation assistant. Help users find music they might enjoy.
            
            CRITICAL INSTRUCTION: You have ONLY ONE tool available called "recommend_music".
            DO NOT attempt to use any calculator tools or any other tools.
            
            The recommend_music tool requires these EXACT parameters:
            - genres: A list of music genres (REQUIRED) - Must be an array containing one or more of: ["pop", "rock", "jazz", "classical", "electronic", "hip_hop"]
            - release_year_min: Minimum release year (optional)
            - release_year_max: Maximum release year (optional)
            - mood: Desired mood (optional) - Must be one of: ["happy", "sad", "energetic", "relaxed", "focused"]
            - limit: Number of recommendations (optional, default 5)
            
            EXAMPLES:
            
            When a user asks for rock and jazz with relaxed mood, your tool call MUST look EXACTLY like this:
            {
              "name": "recommend_music",
              "arguments": {
                "genres": ["rock", "jazz"],
                "mood": "relaxed"
              }
            }
            
            When a user asks for classical music before 1900, your tool call MUST look EXACTLY like this:
            {
              "name": "recommend_music",
              "arguments": {
                "genres": ["classical"],
                "release_year_max": 1900
              }
            }
            
            NEVER use parameters like "operation", "a", or "b" as these are for calculator tools which you DO NOT have access to.
            
            ALWAYS include the "genres" parameter as it is required.
        """)])
    )
    
    # Create a router for the LLM API
    router = get_router(models=("gemini-2.0-flash",))
    
    # Print a note about the expected validation errors
    print("Note: You may see validation errors related to message content being None.")
    print("This is expected behavior when the model makes a tool call and doesn't provide text content.\n")
    
    # Example conversation
    print("Starting conversation with the music recommendation assistant...\n")
    
    # User asks for recommendations
    user_message = LLMUserMessage(parts=[LLMMessagePart(content="Can you recommend some rock and jazz songs with a relaxed mood?")])
    print(f"User: {user_message.parts[0].content}")
    
    result = await agent.step(
        user_message=user_message,
        model="gemini-2.0-flash",
        router=router
    )
    
    print(f"Assistant: {result.assistant_message.parts[0].content}")
    
    if result.tool_message:
        print(f"Tool Result: {result.tool_message}")
    
    # User refines their request
    user_message = LLMUserMessage(parts=[LLMMessagePart(content="How about some classical music from before 1900?")])
    print(f"\nUser: {user_message.parts[0].content}")
    
    result = await agent.step(
        user_message=user_message,
        model="gemini-2.0-flash",
        router=router
    )
    
    print(f"Assistant: {result.assistant_message.parts[0].content}")
    
    if result.tool_message:
        print(f"Tool Result: {result.tool_message}")


if __name__ == "__main__":
    asyncio.run(main())
