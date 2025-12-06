"""
Audio generation service using ElevenLabs text-to-speech API.
"""
import logging
from pathlib import Path
from typing import Optional

from elevenlabs import generate, set_api_key, RateLimitError, APIError
from config.settings import ELEVENLABS_API_KEY, PODCAST_DIR

logger = logging.getLogger(__name__)

set_api_key(ELEVENLABS_API_KEY)

VOICE_CONFIG = {
    "host": "21m00Tcm4TlvDq8ikWAM",
    "guest": "EXAVITQu4vr4xnSDxMaL"
}


async def generate_speech(
    text: str,
    voice_id: str,
    output_filename: str,
    model: str = "eleven_turbo_v2"
) -> str:
    """
    Generate speech from text using ElevenLabs API.
    
    Args:
        text: Text to convert to speech
        voice_id: ElevenLabs voice ID (use VOICE_CONFIG for predefined voices)
        output_filename: Name for output file (e.g., "segment_1.mp3")
        model: ElevenLabs model to use (default: eleven_turbo_v2)
        
    Returns:
        Path to generated audio file
        
    Raises:
        ValueError: If text is empty or voice_id is invalid
        RateLimitError: If API rate limit is exceeded
        APIError: If ElevenLabs API returns an error
        Exception: For other unexpected errors
    """
    if not text or not text.strip():
        raise ValueError("Text cannot be empty")
    
    if not voice_id:
        raise ValueError("Voice ID is required")
    
    if not output_filename:
        raise ValueError("Output filename is required")
    
    try:
        logger.info(f"Generating speech for text length: {len(text)} characters")
        logger.info(f"Using voice ID: {voice_id}")
        
        audio = generate(
            text=text,
            voice=voice_id,
            model=model
        )
        
        PODCAST_DIR.mkdir(parents=True, exist_ok=True)
        
        output_path = PODCAST_DIR / output_filename
        with open(output_path, "wb") as f:
            f.write(audio)
        
        logger.info(f"Audio saved to: {output_path}")
        return str(output_path)
        
    except RateLimitError as e:
        logger.error(f"ElevenLabs rate limit exceeded: {e}")
        raise RateLimitError(
            "Rate limit exceeded. Please wait before making more requests."
        )
    
    except APIError as e:
        logger.error(f"ElevenLabs API error: {e}")
        raise APIError(f"Failed to generate speech: {e}")
    
    except Exception as e:
        logger.error(f"Unexpected error generating speech: {e}")
        raise Exception(f"Failed to generate speech: {e}")


async def generate_podcast_segment(
    text: str,
    speaker: str,
    segment_number: int
) -> str:
    """
    Generate a podcast segment with automatic voice selection.
    
    Args:
        text: Text to convert to speech
        speaker: Either "host" or "guest"
        segment_number: Segment number for filename
        
    Returns:
        Path to generated audio file
        
    Raises:
        ValueError: If speaker is not "host" or "guest"
    """
    if speaker not in VOICE_CONFIG:
        raise ValueError(f"Speaker must be 'host' or 'guest', got: {speaker}")
    
    voice_id = VOICE_CONFIG[speaker]
    output_filename = f"segment_{segment_number}_{speaker}.mp3"
    
    return await generate_speech(
        text=text,
        voice_id=voice_id,
        output_filename=output_filename
    )


def get_available_voices() -> dict:
    """
    Get the configured voice IDs.
    
    Returns:
        Dictionary with host and guest voice IDs
    """
    return VOICE_CONFIG.copy()