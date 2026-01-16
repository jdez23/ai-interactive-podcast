"""
Service for answering questions during podcast playback.

This implements the interactive Q&A feature by combining context
from the podcast and generating natural language answers.
"""

import logging
from typing import Dict, Any
from services.qa_context_builder import build_qa_context, QAContextError
from services.openai_service import generate_completion, OpenAIServiceError

logger = logging.getLogger(__name__)


class QuestionAnswererError(Exception):
    """Custom exception for question answering errors."""
    pass


async def answer_question(
    podcast_id: str,
    question: str,
    timestamp: float
) -> Dict[str, Any]:
    """
    Answer a user's question about podcast content.
    
    This function:
    1. Builds context using qa_context_builder
    2. Generates a natural answer using OpenAI
    3. Returns the answer with metadata
    
    Args:
        podcast_id: ID of the podcast being listened to
        question: User's question
        timestamp: Current playback position in seconds
        
    Returns:
        {
            "answer_text": str,           # The generated answer
            "sources": List[str],         # Source document IDs
            "context_used": {             # Context that was used
                "document_chunks": int,   # Number of chunks used
                "dialogue_exchanges": int # Number of dialogue exchanges used
            },
            "timestamp": float            # Timestamp of the question
        }
        
    Raises:
        QuestionAnswererError: If answer generation fails
        
    Example:
        answer = await answer_question(
            podcast_id="pod_abc123",
            question="What is backpropagation?",
            timestamp=165.5
        )
        print(answer["answer_text"])
    """
    logger.info(f"Answering question for podcast {podcast_id} at {timestamp}s: '{question}'")
    
    try:
        context = await build_qa_context(
            podcast_id=podcast_id,
            question=question,
            timestamp=timestamp
        )
        
        logger.info(
            f"Context built: {len(context['document_chunks'])} chunks, "
            f"{len(context['recent_dialogue'])} dialogue exchanges"
        )
        
        answer_text = await _generate_answer_from_context(context)
        
        sources = list(set(
            chunk.get("source", "unknown")
            for chunk in context["document_chunks"]
        ))
        
        response = {
            "answer_text": answer_text,
            "sources": sources,
            "context_used": {
                "document_chunks": len(context["document_chunks"]),
                "dialogue_exchanges": len(context["recent_dialogue"])
            },
            "timestamp": timestamp
        }
        
        logger.info(f"Successfully generated answer ({len(answer_text)} chars)")
        return response
        
    except QAContextError as e:
        error_msg = f"Failed to build context: {str(e)}"
        logger.error(error_msg)
        raise QuestionAnswererError(error_msg)
    except OpenAIServiceError as e:
        error_msg = f"Failed to generate answer: {str(e)}"
        logger.error(error_msg)
        raise QuestionAnswererError(error_msg)
    except Exception as e:
        error_msg = f"Unexpected error answering question: {str(e)}"
        logger.error(error_msg)
        raise QuestionAnswererError(error_msg)


async def _generate_answer_from_context(context: Dict[str, Any]) -> str:
    """
    Generate an answer using the provided context.
    
    Args:
        context: Context dictionary from build_qa_context
        
    Returns:
        Generated answer text
        
    Raises:
        OpenAIServiceError: If answer generation fails
    """
    question = context["question"]
    document_chunks = context["document_chunks"]
    recent_dialogue = context["recent_dialogue"]
    
    chunks_text = "\n\n".join([
        f"Source: {chunk['source']}\n{chunk['text']}"
        for chunk in document_chunks
    ])
    
    dialogue_text = "\n".join([
        f"[{exchange['timestamp']}s] {exchange['speaker'].upper()}: {exchange['text']}"
        for exchange in recent_dialogue
    ])
    
    prompt = f"""You are answering a listener's question during a podcast.

**Recent Podcast Dialogue:**
{dialogue_text if dialogue_text else "No recent dialogue available."}

**Relevant Information from Source Documents:**
{chunks_text if chunks_text else "No relevant information found in documents."}

**Listener's Question:** {question}

**Instructions:**
1. Answer the question naturally and conversationally, as if you're the podcast host responding
2. Use information from the source documents and recent dialogue
3. If the question relates to something just discussed, reference it naturally
4. Keep your answer concise but complete (2-4 sentences typically)
5. If the sources don't fully answer the question, acknowledge this honestly
6. Don't start with "Great question!" or similar - just answer directly
7. Maintain a friendly, educational tone

Your answer:"""
    
    logger.info("Generating answer with OpenAI...")
    
    try:
        result = generate_completion(
            prompt=prompt,
            model="gpt-4o-mini",
            temperature=0.7,
            max_tokens=300
        )
        
        answer = result["content"].strip()
        
        if not answer:
            raise OpenAIServiceError("Generated answer is empty")
        
        logger.info(f"Generated answer: {len(answer)} characters, {result['usage']['total_tokens']} tokens")
        
        return answer
        
    except Exception as e:
        logger.error(f"Failed to generate answer: {str(e)}")
        raise


def validate_answer(answer: Dict[str, Any]) -> bool:
    """
    Validate that an answer meets quality requirements.
    
    Args:
        answer: Answer dictionary to validate
        
    Returns:
        True if valid, False otherwise
    """
    required_fields = ["answer_text", "sources", "context_used", "timestamp"]
    
    for field in required_fields:
        if field not in answer:
            logger.warning(f"Answer missing required field: {field}")
            return False
    
    if not answer["answer_text"] or len(answer["answer_text"]) < 10:
        logger.warning("Answer text is too short")
        return False
    
    if not isinstance(answer["sources"], list):
        logger.warning("Sources must be a list")
        return False
    
    if not isinstance(answer["context_used"], dict):
        logger.warning("context_used must be a dict")
        return False
    
    logger.info("Answer validation passed")
    return True