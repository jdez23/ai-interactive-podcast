"""
Script generation service for podcast dialogue.

This module transforms document chunks into engaging podcast-style dialogue
between a host and guest, formatted for audio synthesis.
"""

import logging
from typing import List, Dict, Optional
from database.vector_store import get_all_chunks_for_documents
from services.openai_service import generate_completion, estimate_tokens

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ScriptGenerationError(Exception):
    """Custom exception for script generation errors."""
    pass


async def generate_podcast_script(
    document_id: str,
    target_length: str = "medium"
) -> List[Dict]:
    """
    Generate podcast script from document chunks.
    
    This function retrieves document chunks, generates natural dialogue between
    a host and guest, and returns a structured script ready for audio synthesis.
    
    Args:
        document_id: Unique identifier for the document
        target_length: "short" (~2-3 min), "medium" (~5 min), or "long" (~10 min)
        
    Returns:
        List of dialogue exchanges:
        [
            {"speaker": "host", "text": "Welcome to..."},
            {"speaker": "guest", "text": "Thanks for..."},
            ...
        ]
        
    Raises:
        ScriptGenerationError: If script generation fails
        
    Example:
        script = await generate_podcast_script("doc_123", "short")
        for line in script:
            print(f"{line['speaker'].upper()}: {line['text']}")
    """
    logger.info(f"Generating {target_length} podcast script for document {document_id}")
    
    chunks_result = await get_all_chunks_for_documents([document_id])
    
    if chunks_result["status"] == "failed":
        error_msg = chunks_result.get("error", "Unknown error retrieving chunks")
        logger.error(f"Failed to retrieve chunks: {error_msg}")
        raise ScriptGenerationError(f"Failed to retrieve document chunks: {error_msg}")
    
    chunks = chunks_result.get("chunks", [])
    
    if not chunks:
        logger.error(f"No chunks found for document {document_id}")
        raise ScriptGenerationError(f"No content found for document {document_id}")
    
    logger.info(f"Retrieved {len(chunks)} chunks for document {document_id}")
    
    num_chunks = _determine_chunk_count(target_length, len(chunks))
    selected_chunks = chunks[:num_chunks]
    
    logger.info(f"Using {num_chunks} chunks for {target_length} podcast")
    
    combined_content = "\n\n".join(selected_chunks)
    
    estimated_tokens = estimate_tokens(combined_content)
    max_input_tokens = 12000
    
    if estimated_tokens > max_input_tokens:
        logger.warning(f"Content too long ({estimated_tokens} tokens), summarizing...")
        combined_content = await _summarize_content(combined_content, max_input_tokens)
    
    duration_minutes = _get_duration_minutes(target_length)
    dialogue_text = await _generate_dialogue(combined_content, duration_minutes)
    
    script = _parse_dialogue_to_script(dialogue_text)
    
    logger.info(f"Generated script with {len(script)} exchanges")
    
    return script


def _determine_chunk_count(target_length: str, total_chunks: int) -> int:
    """
    Determine how many chunks to use based on target length.
    
    Args:
        target_length: "short", "medium", or "long"
        total_chunks: Total number of available chunks
        
    Returns:
        Number of chunks to use
    """
    chunk_mapping = {
        "short": 3,    # ~2-3 minutes
        "medium": 6,   # ~5 minutes
        "long": 12     # ~10 minutes
    }
    
    desired_chunks = chunk_mapping.get(target_length.lower(), 6)
    
    return min(desired_chunks, total_chunks)


def _get_duration_minutes(target_length: str) -> int:
    """
    Get duration in minutes for target length.
    
    Args:
        target_length: "short", "medium", or "long"
        
    Returns:
        Duration in minutes
    """
    duration_mapping = {
        "short": 3,
        "medium": 5,
        "long": 10
    }
    
    return duration_mapping.get(target_length.lower(), 5)


async def _summarize_content(content: str, max_tokens: int) -> str:
    """
    Summarize content if it exceeds token limits.
    
    Args:
        content: Original content
        max_tokens: Maximum allowed tokens
        
    Returns:
        Summarized content
    """
    logger.info("Summarizing content to fit token limits...")
    
    summarize_prompt = f"""Summarize the following content while preserving all key information, 
facts, and important details. Keep the summary comprehensive but concise.

Content:
{content}

Summary:"""
    
    try:
        result = generate_completion(
            prompt=summarize_prompt,
            model="gpt-4o-mini",
            max_tokens=max_tokens // 2,
            temperature=0.3
        )
        
        return result["content"]
        
    except Exception as e:
        logger.error(f"Failed to summarize content: {str(e)}")
        char_limit = max_tokens * 4 
        return content[:char_limit]


async def _generate_dialogue(content: str, duration_minutes: int) -> str:
    """
    Generate podcast dialogue from content.
    
    Args:
        content: Document content to discuss
        duration_minutes: Target duration in minutes
        
    Returns:
        Raw dialogue text from OpenAI
        
    Raises:
        ScriptGenerationError: If dialogue generation fails
    """
    word_count = duration_minutes * 150
    
    prompt = f"""You are creating a natural, engaging podcast discussion between a host and guest.

**Speakers:**
- Host: Curious, asks insightful questions, represents the learner
- Guest: Knowledgeable expert, explains clearly, makes topics accessible

**Source Material:**
{content}

**Instructions:**
1. Create a {duration_minutes}-minute podcast script (approximately {word_count} words)
2. Start with a warm, engaging introduction
3. Discuss the key points from the source material
4. Use natural conversation with reactions like "wow," "interesting," "that's fascinating"
5. Host should ask follow-up questions that a learner would ask
6. Guest should explain concepts clearly with examples or analogies
7. End with a brief, memorable conclusion
8. Stay true to the source material - don't make up facts
9. Make it sound like a real conversation, not a lecture

**CRITICAL: Format your response EXACTLY like this:**
Host: [Line of dialogue]
Guest: [Response]
Host: [Follow-up]
Guest: [Explanation]
...

Do not include any text outside of the script format. Do not use markdown code blocks. Begin now:
"""
    
    try:
        result = generate_completion(
            prompt=prompt,
            model="gpt-4o-mini",
            temperature=0.7
        )
        
        dialogue = result["content"]
        
        if not dialogue or len(dialogue) < 100:
            raise ScriptGenerationError("Generated dialogue is too short or empty")
        
        return dialogue
        
    except Exception as e:
        logger.error(f"Failed to generate dialogue: {str(e)}")
        raise ScriptGenerationError(f"Dialogue generation failed: {str(e)}")


def _parse_dialogue_to_script(dialogue_text: str) -> List[Dict]:
    """
    Parse raw dialogue text into structured script format.
    
    Args:
        dialogue_text: Raw dialogue from OpenAI (e.g., "Host: Hello\nGuest: Hi")
        
    Returns:
        List of dialogue exchanges with speaker and text
        
    Example:
        Input: "Host: Welcome!\nGuest: Thanks!"
        Output: [
            {"speaker": "host", "text": "Welcome!"},
            {"speaker": "guest", "text": "Thanks!"}
        ]
    """
    script = []
    lines = dialogue_text.strip().split('\n')
    
    for line in lines:
        line = line.strip()
        
        if not line:
            continue
        
        if ':' in line:
            parts = line.split(':', 1)
            speaker_raw = parts[0].strip().lower()
            text = parts[1].strip()
            
            if 'host' in speaker_raw or 'alex' in speaker_raw or 'host a' in speaker_raw:
                speaker = "host"
            elif 'guest' in speaker_raw or 'jordan' in speaker_raw or 'host b' in speaker_raw:
                speaker = "guest"
            else:
                logger.warning(f"Skipping line with unknown speaker: {line[:50]}")
                continue
            
            if text:
                script.append({
                    "speaker": speaker,
                    "text": text
                })
    
    if not script:
        logger.error("Failed to parse any dialogue from generated text")
        raise ScriptGenerationError("Could not parse dialogue into script format")
    
    return script


def validate_script(script: List[Dict]) -> bool:
    """
    Validate that a script meets quality requirements.
    
    Args:
        script: List of dialogue exchanges
        
    Returns:
        True if script is valid, False otherwise
    """
    if not script or len(script) < 4:
        logger.warning("Script too short (less than 4 exchanges)")
        return False
    
    for i, entry in enumerate(script):
        if "speaker" not in entry or "text" not in entry:
            logger.warning(f"Script entry {i} missing required fields")
            return False
        
        if entry["speaker"] not in ["host", "guest"]:
            logger.warning(f"Script entry {i} has invalid speaker: {entry['speaker']}")
            return False
        
        if not entry["text"] or len(entry["text"]) < 10:
            logger.warning(f"Script entry {i} has text that's too short")
            return False
    
    host_count = sum(1 for e in script if e["speaker"] == "host")
    guest_count = sum(1 for e in script if e["speaker"] == "guest")
    
    if host_count == 0 or guest_count == 0:
        logger.warning("Script missing host or guest dialogue")
        return False
    
    logger.info(f"Script validation passed: {len(script)} exchanges, "
                f"{host_count} host, {guest_count} guest")
    
    return True