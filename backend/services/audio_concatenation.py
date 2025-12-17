"""
Audio concatenation service for combining podcast segments.

This module handles combining individual audio segments into a complete podcast.
"""
import logging
from pathlib import Path
from typing import List
from pydub import AudioSegment

logger = logging.getLogger(__name__)


async def concatenate_audio_files(
    audio_files: List[str],
    output_path: str
) -> str:
    """
    Concatenate multiple audio files into a single file.
    
    Args:
        audio_files: List of paths to audio files to concatenate
        output_path: Path where the combined audio should be saved
        
    Returns:
        Path to the concatenated audio file
        
    Raises:
        ValueError: If audio_files is empty
        FileNotFoundError: If any input file doesn't exist
        Exception: If concatenation fails
    """
    if not audio_files:
        raise ValueError("No audio files provided for concatenation")
    
    logger.info(f"Concatenating {len(audio_files)} audio files")
    
    try:
        combined = AudioSegment.empty()
        
        for i, audio_file in enumerate(audio_files):
            file_path = Path(audio_file)
            
            if not file_path.exists():
                raise FileNotFoundError(f"Audio file not found: {audio_file}")
            
            logger.info(f"Loading segment {i+1}/{len(audio_files)}: {file_path.name}")
            segment = AudioSegment.from_mp3(str(file_path))
            combined += segment
        
        output_path_obj = Path(output_path)
        output_path_obj.parent.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Exporting combined audio to: {output_path}")
        combined.export(output_path, format="mp3")
        
        duration_seconds = len(combined) / 1000.0
        logger.info(f"Successfully created podcast: {duration_seconds:.1f} seconds")
        
        return str(output_path)
        
    except FileNotFoundError:
        raise
    except Exception as e:
        error_msg = f"Failed to concatenate audio files: {str(e)}"
        logger.error(error_msg)
        raise Exception(error_msg)


async def get_audio_duration(audio_path: str) -> float:
    """
    Get the duration of an audio file in seconds.
    
    Args:
        audio_path: Path to the audio file
        
    Returns:
        Duration in seconds
        
    Raises:
        FileNotFoundError: If file doesn't exist
        Exception: If duration cannot be determined
    """
    try:
        file_path = Path(audio_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        audio = AudioSegment.from_mp3(str(file_path))
        duration_seconds = len(audio) / 1000.0
        
        return duration_seconds
        
    except FileNotFoundError:
        raise
    except Exception as e:
        error_msg = f"Failed to get audio duration: {str(e)}"
        logger.error(error_msg)
        raise Exception(error_msg)