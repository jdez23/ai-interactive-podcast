"""
API routes for interactive Q&A during podcast playback.

This module handles user questions and generates audio responses.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()


class QuestionRequest(BaseModel):
    """Request model for asking questions."""
    podcast_id: str
    question: str


@router.post("/ask")
async def ask_question(request: QuestionRequest):
    """
    Ask a question about the podcast content.
    
    TODO - Backend Engineer Tasks:
    1. Search vector database for relevant document chunks
    2. If found: Generate answer from documents using LLM
    3. If not found: Use Brave Search API for web results
    4. Generate natural language response
    5. Convert response to audio using ElevenLabs
    6. Return answer audio URL and text
    
    Args:
        request: QuestionRequest with podcast_id and question
        
    Returns:
        {
            "answer_audio_url": "/generated/answers/answer_123.mp3",
            "answer_text": "France played a crucial role...",
            "sources": ["doc_123abc"],
            "used_web_search": false
        }
        
    Raises:
        HTTPException: If podcast not found or answer generation fails
        
    See Also:
        - services/question_answerer.py for Q&A logic
        - database/vector_store.py for searching documents
        - prompts/podcast_prompts.py for answer prompts
    """
    # TODO: Implement question answering
    # Hints:
    # - Use database.vector_store.search_documents(question)
    # - If results found, generate answer from documents
    # - If no results, use Brave Search API
    # - Use prompts.podcast_prompts.QUESTION_ANSWER_PROMPT
    # - Convert answer to speech with ElevenLabs
    # - Save to config.settings.ANSWER_DIR
    
    # STUB: Return placeholder response
    return {
        "answer_audio_url": "http://localhost:8000/generated/answers/stub.mp3",
        "answer_text": f"This is a stub response to: {request.question}",
        "sources": [],
        "used_web_search": False,
        "status": "stub_implementation",
        "message": "TODO: Implement question answering"
    }