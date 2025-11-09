"""
Service for answering questions during podcast playback.

This implements the interactive Q&A feature.
"""

from typing import Dict

# TODO: Import required libraries
# import openai
# import requests  # for ElevenLabs and Brave Search APIs
# from database.vector_store import search_documents
# from prompts.podcast_prompts import QUESTION_ANSWER_PROMPT, WEB_SEARCH_ANSWER_PROMPT


async def answer_question(podcast_id: str, question: str) -> Dict:
    """
    Answer a user's question about podcast content.
    
    TODO - Backend Engineer Tasks:
    
    Step 1: Search documents for relevant information
        - Use database.vector_store.search_documents(question)
        - Get top 3-5 most relevant chunks
        
    Step 2: Decide if we have enough information
        - If relevant chunks found: Generate answer from documents
        - If no relevant chunks: Use web search as fallback
        
    Step 3a: Generate answer from documents
        - Use prompts.podcast_prompts.QUESTION_ANSWER_PROMPT
        - Include relevant chunks as context
        - Call OpenAI API to generate natural response
        
    Step 3b: Or use web search fallback
        - Call Brave Search API with question
        - Use prompts.podcast_prompts.WEB_SEARCH_ANSWER_PROMPT
        - Generate answer from web results
        
    Step 4: Convert answer to audio
        - Call ElevenLabs API to synthesize speech
        - Use Host B voice for consistency
        - Save audio file
        
    Step 5: Return response
        - Return audio URL, text, sources, web_search flag
    
    Args:
        podcast_id: ID of the podcast being listened to
        question: User's question
        
    Returns:
        {
            "answer_audio_url": "/generated/answers/answer_123.mp3",
            "answer_text": "France provided crucial military support...",
            "sources": ["doc_123"],
            "used_web_search": False
        }
        
    Tips:
        - Start with just text responses (skip audio at first)
        - Test document search thoroughly
        - Web search is nice-to-have, focus on documents first
        - Target <5 second response time
        
    Resources:
        - Brave Search API: https://brave.com/search/api/
    """
    # TODO: Implement question answering
    
    raise NotImplementedError("TODO: Implement question answering")