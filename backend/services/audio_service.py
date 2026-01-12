"""
Audio generation service using ElevenLabs text-to-speech API.
"""
import logging
from pathlib import Path
from typing import List, Dict, Optional
import uuid

from elevenlabs import generate, set_api_key, RateLimitError, APIError
from pydub import AudioSegment
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


async def synthesize_audio(
    script: List[Dict],
    output_filename: str,
    pause_duration: int = 500,
    progress_callback = None
) -> str:
    """
    Convert podcast script to audio file.
    
    This function orchestrates the complete audio synthesis pipeline:
    1. Generates individual audio segments for each dialogue line
    2. Adds natural pauses between speaker exchanges
    3. Combines all segments into a single audio file
    4. Cleans up temporary files
    
    Args:
        script: List of dialogue exchanges from generate_podcast_script()
                [{"speaker": "host", "text": "..."}, ...]
        output_filename: Name for output file (e.g., "podcast_123.mp3")
        pause_duration: Duration of pause between speakers in milliseconds (default: 500ms)
        progress_callback: Optional callback function(current, total) for progress updates
        
    Returns:
        Path to generated audio file
        
    Raises:
        ValueError: If script is empty or invalid
        Exception: If audio synthesis fails
        
    Example:
        script = [
            {"speaker": "host", "text": "Welcome to the show!"},
            {"speaker": "guest", "text": "Thanks for having me!"}
        ]
        audio_path = await synthesize_audio(script, "episode_1.mp3")
    """
    if not script:
        raise ValueError("Script cannot be empty")
    
    if not output_filename:
        raise ValueError("Output filename is required")
    
    logger.info(f"Starting audio synthesis for {len(script)} dialogue exchanges")
    
    temp_dir = PODCAST_DIR / "temp"
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    session_id = uuid.uuid4().hex[:8]
    temp_files = []
    
    try:
        logger.info("Generating individual audio segments...")
        for i, line in enumerate(script):
            speaker = line.get("speaker")
            text = line.get("text")
            
            if not speaker or not text:
                logger.warning(f"Skipping invalid script entry at index {i}")
                continue
            
            if speaker not in VOICE_CONFIG:
                logger.warning(f"Unknown speaker '{speaker}' at index {i}, skipping")
                continue
            
            voice_id = VOICE_CONFIG[speaker]
            temp_filename = f"temp_{session_id}_segment_{i:03d}.mp3"
            
            logger.info(f"Generating segment {i+1}/{len(script)}: {speaker}")
            
            segment_path = await generate_speech(
                text=text,
                voice_id=voice_id,
                output_filename=temp_filename
            )
            
            temp_files.append(segment_path)
            
            # Report progress after each segment
            if progress_callback:
                progress_callback(i + 1, len(script))
        
        if not temp_files:
            raise Exception("No audio segments were generated")
        
        logger.info(f"Combining {len(temp_files)} segments with {pause_duration}ms pauses...")
        
        combined = AudioSegment.empty()
        pause = AudioSegment.silent(duration=pause_duration)
        
        for i, segment_path in enumerate(temp_files):
            segment = AudioSegment.from_mp3(segment_path)
            
            combined += segment
            
            if i < len(temp_files) - 1:
                combined += pause
        
        output_path = PODCAST_DIR / output_filename
        logger.info(f"Exporting final audio to: {output_path}")
        
        combined.export(str(output_path), format="mp3")
        
        duration_seconds = len(combined) / 1000.0
        logger.info(f"✅ Audio synthesis complete: {duration_seconds:.1f} seconds")
        
        return str(output_path)
        
    except Exception as e:
        logger.error(f"Audio synthesis failed: {str(e)}")
        raise Exception(f"Failed to synthesize audio: {str(e)}")
        
    finally:
        logger.info("Cleaning up temporary files...")
        for temp_file in temp_files:
            try:
                temp_path = Path(temp_file)
                if temp_path.exists():
                    temp_path.unlink()
                    logger.debug(f"Deleted: {temp_path.name}")
            except Exception as e:
                logger.warning(f"Failed to delete temp file {temp_file}: {e}")
        
        try:
            if temp_dir.exists() and not any(temp_dir.iterdir()):
                temp_dir.rmdir()
                logger.debug("Removed empty temp directory")
        except Exception as e:
            logger.debug(f"Could not remove temp directory: {e}")