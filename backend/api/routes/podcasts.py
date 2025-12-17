"""
API routes for podcast generation.

This module handles generating podcast audio from uploaded documents.
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime
import uuid
import logging
import asyncio
from pathlib import Path

from services.script_generator import generate_podcast_script, validate_script
from services.audio_service import generate_podcast_segment, VOICE_CONFIG
from services.audio_concatenation import concatenate_audio_files, get_audio_duration
from database.vector_store import get_all_chunks_for_documents
from config.settings import PODCAST_DIR

logger = logging.getLogger(__name__)

router = APIRouter()

podcast_storage: Dict[str, Dict] = {}


class GenerationOptions(BaseModel):
    """Options for podcast generation."""
    target_duration: Optional[str] = "medium"


class PodcastGenerateRequest(BaseModel):
    """Request model for podcast generation."""
    document_id: str
    options: Optional[GenerationOptions] = None


class PodcastGenerateResponse(BaseModel):
    """Response model for podcast generation initiation."""
    podcast_id: str
    status: str
    message: str


class PodcastStatusResponse(BaseModel):
    """Response model for podcast status."""
    podcast_id: str
    status: str
    created_at: str
    audio_url: Optional[str] = None
    script_url: Optional[str] = None
    duration_seconds: Optional[float] = None
    error: Optional[str] = None


async def _validate_document_exists(document_id: str) -> bool:
    """
    Validate that a document exists in the vector store.
    
    Args:
        document_id: Document ID to validate
        
    Returns:
        True if document exists, False otherwise
    """
    try:
        result = await get_all_chunks_for_documents([document_id])
        return result["status"] == "success" and len(result.get("chunks", [])) > 0
    except Exception as e:
        logger.error(f"Error validating document {document_id}: {str(e)}")
        return False


async def _generate_podcast_pipeline(
    podcast_id: str,
    document_id: str,
    target_duration: str
):
    """
    Background task to orchestrate the full podcast generation pipeline.
    
    This function runs asynchronously in the background and updates the
    podcast status as it progresses through each stage.
    
    Args:
        podcast_id: Unique podcast identifier
        document_id: Source document ID
        target_duration: Target length (short, medium, long)
    """
    try:
        logger.info(f"Starting podcast generation pipeline for {podcast_id}")
        
        podcast_storage[podcast_id]["status"] = "processing"
        podcast_storage[podcast_id]["stage"] = "generating_script"
        
        logger.info(f"[{podcast_id}] Step 1: Generating script...")
        script = await generate_podcast_script(document_id, target_duration)
        
        if not validate_script(script):
            raise ValueError("Generated script failed validation")
        
        logger.info(f"[{podcast_id}] Script generated with {len(script)} exchanges")
        
        script_path = PODCAST_DIR / f"{podcast_id}_script.json"
        import json
        with open(script_path, "w") as f:
            json.dump(script, f, indent=2)
        
        podcast_storage[podcast_id]["script_url"] = f"/generated/podcasts/{podcast_id}_script.json"
        
        podcast_storage[podcast_id]["stage"] = "generating_audio"
        logger.info(f"[{podcast_id}] Step 2: Generating audio segments...")
        
        audio_files = []
        for i, line in enumerate(script):
            speaker = line["speaker"]
            text = line["text"]
            
            logger.info(f"[{podcast_id}] Generating segment {i+1}/{len(script)} ({speaker})")
            
            audio_path = await generate_podcast_segment(
                text=text,
                speaker=speaker,
                segment_number=i
            )
            
            audio_files.append(audio_path)
        
        logger.info(f"[{podcast_id}] Generated {len(audio_files)} audio segments")
        
        podcast_storage[podcast_id]["stage"] = "concatenating_audio"
        logger.info(f"[{podcast_id}] Step 3: Concatenating audio segments...")
        
        final_audio_path = PODCAST_DIR / f"{podcast_id}.mp3"
        await concatenate_audio_files(audio_files, str(final_audio_path))
        
        duration = await get_audio_duration(str(final_audio_path))
        
        logger.info(f"[{podcast_id}] Cleaning up temporary segment files...")
        for audio_file in audio_files:
            try:
                Path(audio_file).unlink()
            except Exception as e:
                logger.warning(f"Failed to delete segment file {audio_file}: {e}")
        
        podcast_storage[podcast_id].update({
            "status": "complete",
            "stage": "complete",
            "audio_url": f"/generated/podcasts/{podcast_id}.mp3",
            "duration_seconds": duration,
            "completed_at": datetime.utcnow().isoformat() + "Z"
        })
        
        logger.info(f"[{podcast_id}] Podcast generation complete! Duration: {duration:.1f}s")
        
    except Exception as e:
        error_msg = str(e)
        logger.error(f"[{podcast_id}] Pipeline failed: {error_msg}")
        
        podcast_storage[podcast_id].update({
            "status": "failed",
            "stage": "failed",
            "error": error_msg,
            "failed_at": datetime.utcnow().isoformat() + "Z"
        })


@router.post("/generate", response_model=PodcastGenerateResponse, status_code=202)
async def generate_podcast(
    request: PodcastGenerateRequest,
    background_tasks: BackgroundTasks
):
    """
    Generate a podcast from an uploaded document.
    
    This endpoint initiates podcast generation and returns immediately with a
    podcast_id. The actual generation happens in the background. Use the
    GET /api/podcasts/{podcast_id} endpoint to check status.
    
    Args:
        request: PodcastGenerateRequest with document_id and options
        background_tasks: FastAPI background tasks handler
        
    Returns:
        202 Accepted with podcast_id and status
        
    Raises:
        HTTPException 400: If document_id is invalid or doesn't exist
        HTTPException 500: If podcast generation cannot be initiated
        
    Example:
        POST /api/podcasts/generate
        {
            "document_id": "doc_abc123",
            "options": {
                "target_duration": "medium"
            }
        }
        
        Response (202):
        {
            "podcast_id": "pod_xyz789",
            "status": "processing",
            "message": "Podcast generation started"
        }
    """
    try:
        target_duration = "medium"
        if request.options and request.options.target_duration:
            target_duration = request.options.target_duration.lower()
            if target_duration not in ["short", "medium", "long"]:
                raise HTTPException(
                    status_code=400,
                    detail="target_duration must be 'short', 'medium', or 'long'"
                )
        
        podcast_id = f"pod_{uuid.uuid4().hex[:12]}"
        
        podcast_storage[podcast_id] = {
            "podcast_id": podcast_id,
            "status": "processing",
            "stage": "initializing",
            "document_id": request.document_id,
            "target_duration": target_duration,
            "created_at": datetime.utcnow().isoformat() + "Z",
            "audio_url": None,
            "script_url": None,
            "duration_seconds": None,
            "error": None
        }
        
        logger.info(f"Starting background task for podcast {podcast_id}")
        background_tasks.add_task(
            _generate_podcast_pipeline,
            podcast_id,
            request.document_id,
            target_duration
        )
        
        return PodcastGenerateResponse(
            podcast_id=podcast_id,
            status="processing",
            message="Podcast generation started"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to initiate podcast generation: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to initiate podcast generation: {str(e)}"
        )


@router.get("/{podcast_id}", response_model=PodcastStatusResponse)
async def get_podcast(podcast_id: str):
    """
    Get podcast metadata and status.
    
    Use this endpoint to check the status of a podcast generation job
    and retrieve the audio URL once complete.
    
    Args:
        podcast_id: Unique podcast identifier
        
    Returns:
        Podcast metadata including status and audio URL
        
    Raises:
        HTTPException 404: If podcast not found
        
    Example:
        GET /api/podcasts/pod_xyz789
        
        Response (processing):
        {
            "podcast_id": "pod_xyz789",
            "status": "processing",
            "created_at": "2024-01-15T10:30:00Z",
            "audio_url": null,
            "duration_seconds": null
        }
        
        Response (complete):
        {
            "podcast_id": "pod_xyz789",
            "status": "complete",
            "created_at": "2024-01-15T10:30:00Z",
            "audio_url": "/generated/podcasts/pod_xyz789.mp3",
            "script_url": "/generated/podcasts/pod_xyz789_script.json",
            "duration_seconds": 180.5
        }
    """
    if podcast_id not in podcast_storage:
        raise HTTPException(
            status_code=404,
            detail=f"Podcast '{podcast_id}' not found"
        )
    
    podcast_data = podcast_storage[podcast_id]
    
    return PodcastStatusResponse(
        podcast_id=podcast_data["podcast_id"],
        status=podcast_data["status"],
        created_at=podcast_data["created_at"],
        audio_url=podcast_data.get("audio_url"),
        script_url=podcast_data.get("script_url"),
        duration_seconds=podcast_data.get("duration_seconds"),
        error=podcast_data.get("error")
    )


@router.get("/")
async def list_podcasts():
    """
    List all generated podcasts.
    
    Returns:
        List of all podcasts with their metadata
        
    Example:
        GET /api/podcasts/
        
        Response:
        {
            "podcasts": [
                {
                    "podcast_id": "pod_xyz789",
                    "status": "complete",
                    "created_at": "2024-01-15T10:30:00Z",
                    ...
                }
            ],
            "total": 1
        }
    """
    podcasts = list(podcast_storage.values())
    
    return {
        "podcasts": podcasts,
        "total": len(podcasts)
    }