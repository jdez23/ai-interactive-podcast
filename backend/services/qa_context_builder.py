"""
Q&A Context Builder Service.

This module builds context for answering user questions during podcast playback
by gathering relevant document chunks and recent podcast dialogue.
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional

from database.podcast_storage import get_podcast
from database.vector_store import search_documents
from config.settings import PODCAST_DIR

logger = logging.getLogger(__name__)


class QAContextError(Exception):
    """Custom exception for Q&A context building errors."""
    pass


async def build_qa_context(
    podcast_id: str,
    question: str,
    timestamp: float
) -> Dict[str, Any]:
    """
    Build context for answering a question about podcast content.
    
    This function gathers all necessary context to answer a user's question:
    - Relevant document chunks (semantic search)
    - Recent podcast dialogue (based on timestamp)
    - Podcast metadata
    
    Args:
        podcast_id: Unique identifier for the podcast
        question: User's question text
        timestamp: Current playback position in seconds
        
    Returns:
        {
            "question": str,
            "timestamp": float,
            "document_chunks": List[Dict],  # Relevant chunks from source docs
            "recent_dialogue": List[Dict],   # Recent podcast exchanges
            "podcast_metadata": Dict         # Podcast info
        }
        
    Raises:
        QAContextError: If context building fails
        
    Example:
        context = await build_qa_context(
            podcast_id="pod_abc123",
            question="What is backpropagation?",
            timestamp=165.5
        )
    """
    logger.info(f"Building Q&A context for podcast {podcast_id} at timestamp {timestamp}")
    
    if not podcast_id or not podcast_id.strip():
        raise QAContextError("podcast_id cannot be empty")
    
    if not question or not question.strip():
        raise QAContextError("question cannot be empty")
    
    if timestamp < 0:
        raise QAContextError("timestamp cannot be negative")
    
    try:
        podcast_metadata = await _get_podcast_metadata(podcast_id)
        
        document_chunks = await _search_relevant_chunks(
            question=question,
            document_ids=podcast_metadata.get("document_ids", []),
            n_results=5
        )
        
        script = await _load_podcast_script(podcast_id)
        
        recent_dialogue = _extract_recent_dialogue(
            script=script,
            timestamp=timestamp,
            lookback_seconds=60
        )
        
        context = {
            "question": question.strip(),
            "timestamp": timestamp,
            "document_chunks": document_chunks,
            "recent_dialogue": recent_dialogue,
            "podcast_metadata": {
                "podcast_id": podcast_metadata["podcast_id"],
                "document_ids": podcast_metadata.get("document_ids", []),
                "created_at": podcast_metadata.get("created_at")
            }
        }
        
        logger.info(
            f"Successfully built context: {len(document_chunks)} chunks, "
            f"{len(recent_dialogue)} dialogue exchanges"
        )
        
        return context
        
    except QAContextError:
        raise
    except Exception as e:
        error_msg = f"Failed to build Q&A context: {str(e)}"
        logger.error(error_msg)
        raise QAContextError(error_msg)


async def _get_podcast_metadata(podcast_id: str) -> Dict[str, Any]:
    """
    Retrieve podcast metadata from database.
    
    Args:
        podcast_id: Unique podcast identifier
        
    Returns:
        Podcast metadata dictionary
        
    Raises:
        QAContextError: If podcast not found or retrieval fails
    """
    logger.info(f"Retrieving metadata for podcast {podcast_id}")
    
    try:
        podcast = get_podcast(podcast_id)
        
        if podcast is None:
            raise QAContextError(f"Podcast {podcast_id} not found")
        
        if podcast.get("status") != "complete":
            logger.warning(
                f"Podcast {podcast_id} has status '{podcast.get('status')}', "
                "Q&A may not work properly"
            )
        
        logger.info(f"Retrieved metadata for podcast {podcast_id}")
        return podcast
        
    except QAContextError:
        raise
    except Exception as e:
        error_msg = f"Failed to retrieve podcast metadata: {str(e)}"
        logger.error(error_msg)
        raise QAContextError(error_msg)


async def _search_relevant_chunks(
    question: str,
    document_ids: List[str],
    n_results: int = 5
) -> List[Dict[str, Any]]:
    """
    Search for relevant document chunks using semantic search.
    
    Args:
        question: User's question
        document_ids: List of document IDs to search within
        n_results: Number of chunks to return
        
    Returns:
        List of relevant chunks with metadata:
        [
            {
                "text": "chunk content...",
                "source": "document.pdf",
                "relevance_score": 0.95
            },
            ...
        ]
        
    Raises:
        QAContextError: If search fails
    """
    logger.info(f"Searching for relevant chunks: '{question}' (n_results={n_results})")
    
    if not document_ids:
        logger.warning("No document IDs provided, returning empty chunks")
        return []
    
    try:
        search_result = await search_documents(
            query=question,
            document_ids=document_ids,
            n_results=n_results
        )
        
        if search_result["status"] == "failed":
            error_msg = search_result.get("error", "Unknown search error")
            raise QAContextError(f"Document search failed: {error_msg}")
        
        chunks = search_result.get("chunks", [])
        metadatas = search_result.get("metadatas", [])
        
        formatted_chunks = []
        for i, chunk_text in enumerate(chunks):
            metadata = metadatas[i] if i < len(metadatas) else {}
            
            formatted_chunks.append({
                "text": chunk_text,
                "source": metadata.get("source", "unknown"),
                "relevance_score": 1.0 - (i * 0.1)
            })
        
        logger.info(f"Found {len(formatted_chunks)} relevant chunks")
        return formatted_chunks
        
    except QAContextError:
        raise
    except Exception as e:
        error_msg = f"Failed to search document chunks: {str(e)}"
        logger.error(error_msg)
        raise QAContextError(error_msg)


async def _load_podcast_script(podcast_id: str) -> List[Dict[str, str]]:
    """
    Load podcast script from JSON file.
    
    Args:
        podcast_id: Unique podcast identifier
        
    Returns:
        List of dialogue exchanges:
        [
            {"speaker": "host", "text": "Welcome..."},
            {"speaker": "guest", "text": "Thanks..."},
            ...
        ]
        
    Raises:
        QAContextError: If script file not found or invalid
    """
    script_path = PODCAST_DIR / f"{podcast_id}_script.json"
    
    logger.info(f"Loading script from {script_path}")
    
    if not script_path.exists():
        raise QAContextError(f"Script file not found: {script_path}")
    
    try:
        with open(script_path, 'r', encoding='utf-8') as f:
            script = json.load(f)
        
        if not isinstance(script, list):
            raise QAContextError("Script must be a list of dialogue exchanges")
        
        if not script:
            raise QAContextError("Script is empty")
        
        for i, entry in enumerate(script):
            if not isinstance(entry, dict):
                raise QAContextError(f"Script entry {i} is not a dictionary")
            if "speaker" not in entry or "text" not in entry:
                raise QAContextError(f"Script entry {i} missing 'speaker' or 'text'")
        
        logger.info(f"Loaded script with {len(script)} exchanges")
        return script
        
    except json.JSONDecodeError as e:
        error_msg = f"Invalid JSON in script file: {str(e)}"
        logger.error(error_msg)
        raise QAContextError(error_msg)
    except QAContextError:
        raise
    except Exception as e:
        error_msg = f"Failed to load script: {str(e)}"
        logger.error(error_msg)
        raise QAContextError(error_msg)


def _extract_recent_dialogue(
    script: List[Dict[str, str]],
    timestamp: float,
    lookback_seconds: float = 60
) -> List[Dict[str, Any]]:
    """
    Extract recent dialogue based on timestamp.
    
    This function estimates which dialogue exchanges occurred recently
    based on the current playback position.
    
    Args:
        script: Full podcast script
        timestamp: Current playback position in seconds
        lookback_seconds: How far back to look (default: 60 seconds)
        
    Returns:
        List of recent dialogue exchanges with estimated timestamps:
        [
            {
                "speaker": "host",
                "text": "So how do neural networks learn?",
                "timestamp": 155.0
            },
            ...
        ]
        
    Algorithm:
        1. Estimate average seconds per exchange (8 seconds)
        2. Calculate which exchanges fall within lookback window
        3. Return those exchanges with estimated timestamps
    """
    if not script:
        logger.warning("Empty script provided to _extract_recent_dialogue")
        return []
    
    # This is a simple estimate - can be tuned based on actual audio
    SECONDS_PER_EXCHANGE = 8.0
    
    total_exchanges = len(script)
    estimated_total_duration = total_exchanges * SECONDS_PER_EXCHANGE
    
    if timestamp > estimated_total_duration:
        logger.warning(
            f"Timestamp {timestamp}s exceeds estimated duration {estimated_total_duration}s, "
            "using last exchanges"
        )
        timestamp = estimated_total_duration
    
    current_exchange_index = int(timestamp / SECONDS_PER_EXCHANGE)
    current_exchange_index = min(current_exchange_index, total_exchanges - 1)
    
    lookback_exchanges = int(lookback_seconds / SECONDS_PER_EXCHANGE)
    lookback_exchanges = max(lookback_exchanges, 1)
    
    start_index = max(0, current_exchange_index - lookback_exchanges + 1)
    end_index = current_exchange_index + 1
    
    recent_exchanges = script[start_index:end_index]
    
    recent_dialogue = []
    for i, exchange in enumerate(recent_exchanges):
        exchange_index = start_index + i
        estimated_timestamp = exchange_index * SECONDS_PER_EXCHANGE
        
        recent_dialogue.append({
            "speaker": exchange["speaker"],
            "text": exchange["text"],
            "timestamp": round(estimated_timestamp, 1)
        })
    
    logger.info(
        f"Extracted {len(recent_dialogue)} recent exchanges "
        f"(from index {start_index} to {end_index-1})"
    )
    
    return recent_dialogue


def validate_context(context: Dict[str, Any]) -> bool:
    """
    Validate that a context object meets requirements.
    
    Args:
        context: Context dictionary to validate
        
    Returns:
        True if valid, False otherwise
    """
    required_fields = [
        "question",
        "timestamp",
        "document_chunks",
        "recent_dialogue",
        "podcast_metadata"
    ]
    
    for field in required_fields:
        if field not in context:
            logger.warning(f"Context missing required field: {field}")
            return False
    
    if not isinstance(context["document_chunks"], list):
        logger.warning("document_chunks must be a list")
        return False
    
    if not isinstance(context["recent_dialogue"], list):
        logger.warning("recent_dialogue must be a list")
        return False
    
    if not isinstance(context["podcast_metadata"], dict):
        logger.warning("podcast_metadata must be a dict")
        return False
    
    logger.info("Context validation passed")
    return True