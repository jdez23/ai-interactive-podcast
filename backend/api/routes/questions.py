"""
API routes for interactive Q&A during podcast playback.

This module handles user questions and generates text responses.
"""

import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.question_answerer import answer_question, QuestionAnswererError

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
    Ask a question about the podcast content.
    
    This endpoint:
    1. Builds context from podcast content and recent dialogue
    2. Generates a natural language answer using OpenAI
    3. Returns the answer with source information
    
    Args:
        request: QuestionRequest with podcast_id, question, and timestamp
        
    Returns:
        {
            "answer_text": "Backpropagation is an algorithm...",
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
            timestamp=request.timestamp
        )
        
        logger.info(f"Successfully answered question for podcast {request.podcast_id}")
        return answer
        
    except QuestionAnswererError as e:
        logger.error(f"Failed to answer question: {str(e)}")
        
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        
        raise HTTPException(status_code=500, detail=f"Failed to generate answer: {str(e)}")
    
    except Exception as e:
        logger.error(f"Unexpected error in ask_question: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")