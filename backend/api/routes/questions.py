"""
API routes for interactive Q&A during podcast playback.

This module handles user questions and generates text responses.
"""

import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.question_answerer import answer_question, QuestionAnswererError
from services.qa_audio_transitions import (
    generate_acknowledgment_audio,
    generate_return_transition_audio
)

logger = logging.getLogger(__name__)
router = APIRouter()


class QuestionRequest(BaseModel):
    """Request model for asking questions."""
    podcast_id: str
    question: str
    timestamp: float


@router.post("/ask")
async def ask_question(request: QuestionRequest):
    """
    Ask a question about the podcast content with conversational audio response.
    
    This endpoint:
    1. Builds context from podcast content and recent dialogue
    2. Generates a conversational podcast-style answer using OpenAI
    3. Generates audio response with podcast host voice
    4. Returns the answer with source information and audio URL
    
    Args:
        request: QuestionRequest with podcast_id, question, and timestamp
        
    Returns:
        {
            "answer_text": "Looks like we have a question from one of our listeners! Go ahead...",
            "answer_only": "Backpropagation is an algorithm...",
            "audio_url": "generated/podcasts/answer_pod123_abc.mp3",
            "sources": ["machine_learning.pdf"],
            "context_used": {
                "document_chunks": 5,
                "dialogue_exchanges": 3
            },
            "timestamp": 165.5
        }
        
    Raises:
        HTTPException: If podcast not found or answer generation fails
    """
    logger.info(
        f"Received question for podcast {request.podcast_id} "
        f"at {request.timestamp}s: '{request.question}'"
    )
    
    if not request.question or not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
    if request.timestamp < 0:
        raise HTTPException(status_code=400, detail="Timestamp cannot be negative")
    
    try:
        answer = await answer_question(
            podcast_id=request.podcast_id,
            question=request.question.strip(),
            timestamp=request.timestamp,
            generate_audio=True
        )
        
        logger.info(
            f"Successfully answered question for podcast {request.podcast_id} "
            f"with audio: {answer.get('audio_url', 'N/A')}"
        )
        return answer
        
    except QuestionAnswererError as e:
        logger.error(f"Failed to answer question: {str(e)}")
        
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        
        raise HTTPException(status_code=500, detail=f"Failed to generate answer: {str(e)}")
    
    except Exception as e:
        logger.error(f"Unexpected error in ask_question: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


class AcknowledgmentRequest(BaseModel):
    """Request model for acknowledgment with question."""
    question: str


@router.post("/acknowledgment")
async def get_acknowledgment(request: AcknowledgmentRequest):
    """
    Generate acknowledgment audio that includes reading the question.
    
    This endpoint generates:
    - Acknowledgment phrase: "Oh, looks like we have a question from one of our listeners..."
    - Question reading: "They're asking: [question]"
    - Combined audio file
    
    Args:
        request: AcknowledgmentRequest with the question text
    
    Returns:
        {
            "acknowledgment_text": str,
            "question_text": str,
            "full_text": str,
            "audio_url": str
        }
        
    Raises:
        HTTPException: If audio generation fails
    """
    logger.info(f"Generating acknowledgment audio for question: '{request.question}'")
    
    try:
        result = await generate_acknowledgment_audio(question=request.question)
        logger.info(f"Successfully generated acknowledgment audio: {result['audio_url']}")
        return result
        
    except Exception as e:
        logger.error(f"Failed to generate acknowledgment audio: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate acknowledgment: {str(e)}")


@router.post("/return-transition")
async def get_return_transition():
    """
    Generate transition audio to return to the podcast.
    
    This endpoint generates a natural transition phrase like:
    - "Alright, let's get back to it!"
    - "Now, where were we..."
    
    Returns:
        {
            "text": str,
            "audio_url": str
        }
        
    Raises:
        HTTPException: If audio generation fails
    """
    logger.info("Generating return transition audio")
    
    try:
        result = await generate_return_transition_audio()
        logger.info(f"Successfully generated return transition audio: {result['audio_url']}")
        return result
        
    except Exception as e:
        logger.error(f"Failed to generate return transition audio: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate transition: {str(e)}")