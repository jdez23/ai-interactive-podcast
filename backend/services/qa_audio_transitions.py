"""
Service for generating Q&A audio transitions for smooth podcast flow.

This module handles generating acknowledgment and transition audio clips
to make the Q&A experience feel like a natural 3-way conversation.
"""

import logging
import random
from services.audio_service import generate_speech, VOICE_CONFIG

logger = logging.getLogger(__name__)

ACKNOWLEDGMENT_PHRASES = [
    "Oh, looks like we have a question from one of our listeners!",
    "I see we have a listener question coming in!",
    "Ah, great! We've got a question from our audience!",
    "Oh wonderful, a listener wants to ask something!",
]

INVITATION_PHRASES = [
    "Go ahead, what's your question?",
    "Let's hear it!",
    "What would you like to know?",
    "Fire away!",
]

RETURN_PHRASES = [
    "Alright, let's get back to it!",
    "Now, where were we...",
    "Great! Let's continue.",
    "Perfect! Back to our discussion.",
    "Okay, let's pick up where we left off.",
]


async def generate_acknowledgment_audio(question: str) -> dict:
    """
    Generate acknowledgment audio that includes reading the question.
    
    This creates a natural podcast-style acknowledgment:
    1. Acknowledgment: "Oh, looks like we have a question..."
    2. Question reading: "They're asking: [question]"
    
    Args:
        question: The question text to include in the acknowledgment
    
    Returns:
        {
            "acknowledgment_text": str,
            "question_text": str,
            "full_text": str,
            "audio_url": str
        }
    """
    try:
        acknowledgment = random.choice(ACKNOWLEDGMENT_PHRASES)
        question_intro = f"They're asking: {question}"
        full_text = f"{acknowledgment} {question_intro}"
        
        logger.info(f"Generating acknowledgment audio with question: {full_text}")
        
        filename = "acknowledgment_temp.mp3"
        audio_path = await generate_speech(
            text=full_text,
            voice_id=VOICE_CONFIG["host"],
            output_filename=filename,
            model="eleven_turbo_v2"
        )
        
        relative_path = f"generated/podcasts/{filename}"
        
        return {
            "acknowledgment_text": acknowledgment,
            "question_text": question_intro,
            "full_text": full_text,
            "audio_url": relative_path
        }
        
    except Exception as e:
        logger.error(f"Failed to generate acknowledgment audio: {str(e)}")
        raise Exception(f"Acknowledgment audio generation failed: {str(e)}")


async def generate_return_transition_audio() -> dict:
    """
    Generate transition audio to return to the podcast.
    
    Returns:
        {
            "text": str,
            "audio_url": str
        }
    """
    try:
        return_text = random.choice(RETURN_PHRASES)
        
        logger.info(f"Generating return transition audio: {return_text}")
        
        filename = "return_temp.mp3"
        audio_path = await generate_speech(
            text=return_text,
            voice_id=VOICE_CONFIG["host"],
            output_filename=filename,
            model="eleven_turbo_v2"
        )
        
        relative_path = f"generated/podcasts/{filename}"
        
        return {
            "text": return_text,
            "audio_url": relative_path
        }
        
    except Exception as e:
        logger.error(f"Failed to generate return transition audio: {str(e)}")
        raise Exception(f"Return transition audio generation failed: {str(e)}")
