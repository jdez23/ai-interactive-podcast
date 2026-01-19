"""
Service for answering questions during podcast playback.

This implements the interactive Q&A feature by combining context
from the podcast and generating natural language answers.
"""

import logging
import uuid
from pathlib import Path
from typing import Dict, Any
from services.qa_context_builder import build_qa_context, QAContextError
from services.openai_service import generate_completion, OpenAIServiceError
from services.audio_service import generate_speech, VOICE_CONFIG
from config.settings import PODCAST_DIR

logger = logging.getLogger(__name__)

ANSWERS_DIR = Path("backend/generated/answers")
ANSWERS_DIR.mkdir(parents=True, exist_ok=True)


class QuestionAnswererError(Exception):
    """Custom exception for question answering errors."""
    pass


async def answer_question(
    podcast_id: str,
    question: str,
    timestamp: float,
    generate_audio: bool = True
) -> Dict[str, Any]:
    """
    Answer a user's question about podcast content with conversational podcast-style audio.
    
    This function:
    1. Builds context using qa_context_builder
    2. Generates conversational acknowledgment and answer using OpenAI
    3. Generates audio response with podcast host voice
    4. Returns the answer with metadata and audio URL
    
    Args:
        podcast_id: ID of the podcast being listened to
        question: User's question
        timestamp: Current playback position in seconds
        generate_audio: Whether to generate audio response (default: True)
        
    Returns:
        {
            "answer_text": str,           # The full conversational response
            "answer_only": str,           # Just the answer without acknowledgment
            "audio_url": str,             # URL to audio file (if generate_audio=True)
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
        print(answer["audio_url"])
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
        
        conversational_response = await _generate_conversational_response(context, question)
        
        sources = list(set(
            chunk.get("source", "unknown")
            for chunk in context["document_chunks"]
        ))
        
        response = {
            "answer_text": conversational_response["full_text"],
            "answer_only": conversational_response["answer_only"],
            "sources": sources,
            "context_used": {
                "document_chunks": len(context["document_chunks"]),
                "dialogue_exchanges": len(context["recent_dialogue"])
            },
            "timestamp": timestamp
        }
        
        if generate_audio:
            audio_url = await _generate_answer_audio(
                podcast_id=podcast_id,
                full_text=conversational_response["full_text"]
            )
            response["audio_url"] = audio_url
            logger.info(f"Generated audio response: {audio_url}")
        
        logger.info(f"Successfully generated answer ({len(conversational_response['full_text'])} chars)")
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


async def _generate_conversational_response(context: Dict[str, Any], question: str) -> Dict[str, str]:
    """
    Generate a conversational podcast-style response with acknowledgment and answer.
    
    Args:
        context: Context dictionary from build_qa_context
        question: The user's question
        
    Returns:
        {
            "full_text": str,      # Complete response with acknowledgment
            "answer_only": str     # Just the answer part
        }
        
    Raises:
        OpenAIServiceError: If answer generation fails
    """
    document_chunks = context["document_chunks"]
    recent_dialogue = context["recent_dialogue"]
    
    chunks_text = "\n\n".join([
        f"Source: {chunk['source']}\n{chunk['text']}"
        for chunk in document_chunks
    ])
    
    dialogue_text = "\n".join([
        f"[{exchange['timestamp']}s] {exchange['text']}"
        for exchange in recent_dialogue
    ])
    
    prompt = f"""You are a podcast host responding to a live listener question during your show.

**Recent Podcast Dialogue:**
{dialogue_text if dialogue_text else "No recent dialogue available."}

**Relevant Information from Source Documents:**
{chunks_text if chunks_text else "No relevant information found in documents."}

**Listener's Question:** {question}

**Instructions:**
The listener has just asked their question. Generate a natural, conversational answer that includes:

1. A brief reaction/filler (1 sentence)
   - Examples: "Wow, that's a great question!"
   - Or: "Ooh, that's an interesting one!"
   - Or: "That's a really important topic!"

2. The actual answer (2-4 sentences)
   - Answer naturally and conversationally
   - Use information from the source documents and recent dialogue
   - If the question relates to something just discussed, reference it
   - If sources don't fully answer, acknowledge honestly
   - Maintain a friendly, educational tone

DO NOT include any speaker labels like "HOST:" or "GUEST:" in your response.
Format your response as natural speech, like you're talking directly to the listener.

Your response:"""
    
    logger.info("Generating conversational response with OpenAI...")
    
    try:
        result = generate_completion(
            prompt=prompt,
            model="gpt-4o-mini",
            temperature=0.8,
            max_tokens=400
        )
        
        full_text = result["content"].strip()
        
        if not full_text:
            raise OpenAIServiceError("Generated response is empty")
        
        logger.info(f"Generated response: {len(full_text)} characters, {result['usage']['total_tokens']} tokens")
        
        answer_only = full_text
        
        return {
            "full_text": full_text,
            "answer_only": answer_only
        }
        
    except Exception as e:
        logger.error(f"Failed to generate conversational response: {str(e)}")
        raise


async def _generate_answer_audio(podcast_id: str, full_text: str) -> str:
    """
    Generate audio for the conversational answer using podcast host voice.
    
    Args:
        podcast_id: ID of the podcast (for organizing files)
        full_text: The complete conversational response text
        
    Returns:
        Relative URL path to the generated audio file
        
    Raises:
        Exception: If audio generation fails
    """
    try:
        answer_id = uuid.uuid4().hex[:12]
        filename = f"answer_{podcast_id}_{answer_id}.mp3"
        
        logger.info(f"Generating audio for answer: {filename}")
        
        voice_id = VOICE_CONFIG["host"]
        
        audio_path = await generate_speech(
            text=full_text,
            voice_id=voice_id,
            output_filename=filename,
            model="eleven_turbo_v2"
        )
        
        relative_path = f"generated/podcasts/{filename}"
        logger.info(f"Audio generated successfully: {relative_path}")
        
        return relative_path
        
    except Exception as e:
        logger.error(f"Failed to generate answer audio: {str(e)}")
        raise Exception(f"Audio generation failed: {str(e)}")


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
    
    if "audio_url" in answer and not isinstance(answer["audio_url"], str):
        logger.warning("audio_url must be a string")
        return False
    
    logger.info("Answer validation passed")
    return True