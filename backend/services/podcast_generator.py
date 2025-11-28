"""
Service for generating podcast audio from documents.

This is the most complex service - take your time implementing it!
"""

from typing import List, Dict

# TODO: Import required libraries
# import openai
# import requests  # for ElevenLabs API
# from database.vector_store import search_documents
# from prompts.podcast_prompts import PODCAST_SCRIPT_PROMPT
# from config.settings import OPENAI_API_KEY, ELEVENLABS_API_KEY


async def generate_podcast_from_documents(
    document_ids: List[str],
    topic: str,
    duration_minutes: int
) -> Dict:
    """
    Generate a complete podcast from documents.
    
    TODO - Backend Engineer Tasks:
    This is a BIG function. Break it into steps:
    
    Step 1: Retrieve relevant document chunks
        - Use database.vector_store.get_all_chunks_for_documents(document_ids)
        - Or use search_documents(topic, document_ids)
        - Check result["status"] == "success" before using chunks
        - Handle errors gracefully if status is "failed"
        
    Step 2: Generate podcast script using LLM
        - Use prompts.podcast_prompts.PODCAST_SCRIPT_PROMPT
        - Fill in template with topic and document chunks
        - Call OpenAI API to generate script
        
    Step 3: Parse script into host lines
        - Split by "Host A:" and "Host B:"
        - Create list of {host: "A", text: "..."} objects
        
    Step 4: Generate audio for each line
        - Call ElevenLabs API for each line
        - Use different voice IDs for Host A and Host B
        - Save each audio segment
        
    Step 5: Concatenate audio files
        - Use pydub to combine audio segments
        - Save final podcast MP3
        
    Step 6: Return podcast metadata
        - Generate unique podcast_id
        - Return audio URL, script, duration
    
    Args:
        document_ids: List of document IDs to use as sources
        topic: Podcast topic
        duration_minutes: Target length in minutes
        
    Returns:
        {
            "podcast_id": "podcast_xyz",
            "audio_url": "/generated/podcasts/podcast_xyz.mp3",
            "script": "Host A: Welcome...",
            "duration_seconds": 180
        }
        
    Tips:
        - Start by just generating the script (Steps 1-2)
        - Test script quality before moving to audio
        - Pre-generate a test podcast for demo day backup
        - This will take the most time - budget 1-2 weeks
        
    Resources:
        - OpenAI API: https://platform.openai.com/docs/api-reference
        - ElevenLabs API: https://elevenlabs.io/docs/api-reference/text-to-speech
        - Pydub: https://github.com/jiaaro/pydub
    """
    # TODO: Implement podcast generation
    
    raise NotImplementedError("TODO: Implement podcast generation - this is the big one!")


def parse_podcast_script(script: str) -> List[Dict]:
    """
    Parse podcast script into individual host lines.
    
    TODO - Backend Engineer Tasks:
    1. Split script by newlines
    2. For each line, check if it starts with "Host A:" or "Host B:"
    3. Extract the text after the host marker
    4. Return list of {host: "A", text: "..."} dictionaries
    
    Args:
        script: Full podcast script
        
    Returns:
        [
            {"host": "A", "text": "Welcome to today's episode!"},
            {"host": "B", "text": "Thanks for having me!"},
            ...
        ]
        
    Example Script Format:
        Host A: Welcome to today's learning session about the American Revolution!
        Host B: Thanks! I'm excited to discuss this fascinating period.
        Host A: Let's start with the causes...
    """
    # TODO: Implement script parsing
    
    raise NotImplementedError("TODO: Implement script parsing")