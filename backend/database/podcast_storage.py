"""
Podcast metadata storage using SQLite.

This module provides persistent storage for podcast metadata, including
status tracking, audio URLs, and error handling.
"""

import sqlite3
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List
import logging

from config.settings import PODCAST_DIR

logger = logging.getLogger(__name__)

DB_PATH = Path(__file__).parent / "podcasts.db"


def _get_connection() -> sqlite3.Connection:
    """
    Get a database connection with row factory enabled.
    
    Returns:
        SQLite connection object
    """
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_database() -> None:
    """
    Initialize the podcast database with required schema.
    
    Creates the podcasts table if it doesn't exist.
    """
    conn = _get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS podcasts (
                podcast_id TEXT PRIMARY KEY,
                document_ids TEXT NOT NULL,
                status TEXT NOT NULL,
                progress_percentage INTEGER DEFAULT 0,
                stage TEXT,
                target_duration TEXT,
                audio_url TEXT,
                script_url TEXT,
                duration_seconds REAL,
                created_at TEXT NOT NULL,
                completed_at TEXT,
                failed_at TEXT,
                error_message TEXT
            )
        """)
        conn.commit()
        logger.info(f"Database initialized at {DB_PATH}")
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}")
        raise
    finally:
        conn.close()


def save_podcast(podcast_data: Dict) -> None:
    """
    Save or update podcast metadata.
    
    Args:
        podcast_data: Dictionary containing podcast metadata
            Required fields:
            - podcast_id: Unique identifier
            - status: Current status (processing, complete, failed)
            - created_at: ISO timestamp
            Optional fields:
            - progress_percentage: Progress from 0-100
            - document_ids: List of document IDs (will be JSON serialized)
            - stage: Current processing stage
            - target_duration: Target length (short, medium, long)
            - audio_url: URL to generated audio file
            - script_url: URL to script JSON file
            - duration_seconds: Audio duration in seconds
            - completed_at: ISO timestamp when completed
            - failed_at: ISO timestamp when failed
            - error_message: Error description if failed
    
    Raises:
        ValueError: If required fields are missing
    """
    required_fields = ["podcast_id", "status", "created_at"]
    for field in required_fields:
        if field not in podcast_data:
            raise ValueError(f"Missing required field: {field}")
    
    document_ids = podcast_data.get("document_ids", [])
    if isinstance(document_ids, list):
        document_ids = json.dumps(document_ids)
    
    conn = _get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO podcasts (
                podcast_id, document_ids, status, progress_percentage, stage, target_duration,
                audio_url, script_url, duration_seconds,
                created_at, completed_at, failed_at, error_message
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            podcast_data["podcast_id"],
            document_ids,
            podcast_data["status"],
            podcast_data.get("progress_percentage", 0),
            podcast_data.get("stage"),
            podcast_data.get("target_duration"),
            podcast_data.get("audio_url"),
            podcast_data.get("script_url"),
            podcast_data.get("duration_seconds"),
            podcast_data["created_at"],
            podcast_data.get("completed_at"),
            podcast_data.get("failed_at"),
            podcast_data.get("error_message")
        ))
        conn.commit()
        logger.info(f"Saved podcast {podcast_data['podcast_id']} with status {podcast_data['status']}")
    except Exception as e:
        logger.error(f"Failed to save podcast {podcast_data.get('podcast_id')}: {str(e)}")
        raise
    finally:
        conn.close()


def get_podcast(podcast_id: str) -> Optional[Dict]:
    """
    Retrieve podcast metadata by ID.
    
    Args:
        podcast_id: Unique podcast identifier
        
    Returns:
        Dictionary containing podcast metadata, or None if not found
    """
    conn = _get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM podcasts WHERE podcast_id = ?
        """, (podcast_id,))
        
        row = cursor.fetchone()
        if row is None:
            return None
        
        podcast = dict(row)
        
        if podcast.get("document_ids"):
            try:
                podcast["document_ids"] = json.loads(podcast["document_ids"])
            except json.JSONDecodeError:
                podcast["document_ids"] = [podcast["document_ids"]]
        
        return podcast
    except Exception as e:
        logger.error(f"Failed to retrieve podcast {podcast_id}: {str(e)}")
        raise
    finally:
        conn.close()


def get_all_podcasts() -> List[Dict]:
    """
    Get all podcasts ordered by creation date (newest first).
    
    Returns:
        List of podcast metadata dictionaries
    """
    conn = _get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM podcasts ORDER BY created_at DESC
        """)
        
        rows = cursor.fetchall()
        podcasts = []
        
        for row in rows:
            podcast = dict(row)
            
            if podcast.get("document_ids"):
                try:
                    podcast["document_ids"] = json.loads(podcast["document_ids"])
                except json.JSONDecodeError:
                    podcast["document_ids"] = [podcast["document_ids"]]
            
            podcasts.append(podcast)
        
        return podcasts
    except Exception as e:
        logger.error(f"Failed to retrieve all podcasts: {str(e)}")
        raise
    finally:
        conn.close()


def update_podcast_status(
    podcast_id: str,
    status: str,
    progress_percentage: int = None,
    **kwargs
) -> None:
    """
    Update podcast status and optional fields.
    
    Args:
        podcast_id: Unique podcast identifier
        status: New status (processing, complete, failed)
        progress_percentage: Progress from 0-100 (optional)
        **kwargs: Additional fields to update (e.g., audio_url, error_message)
    
    Raises:
        ValueError: If podcast doesn't exist
    """
    existing = get_podcast(podcast_id)
    if existing is None:
        raise ValueError(f"Podcast {podcast_id} not found")
    
    existing["status"] = status
    
    if progress_percentage is not None:
        existing["progress_percentage"] = progress_percentage
    
    for key, value in kwargs.items():
        existing[key] = value
    
    if status == "complete" and "completed_at" not in kwargs:
        existing["completed_at"] = datetime.utcnow().isoformat() + "Z"
    elif status == "failed" and "failed_at" not in kwargs:
        existing["failed_at"] = datetime.utcnow().isoformat() + "Z"
    
    save_podcast(existing)


def delete_podcast(podcast_id: str) -> None:
    """
    Delete podcast metadata from database.
    
    Note: This does NOT delete the actual audio/script files.
    Use cleanup_failed_podcast() for complete cleanup.
    
    Args:
        podcast_id: Unique podcast identifier
    """
    conn = _get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            DELETE FROM podcasts WHERE podcast_id = ?
        """, (podcast_id,))
        conn.commit()
        logger.info(f"Deleted podcast {podcast_id} from database")
    except Exception as e:
        logger.error(f"Failed to delete podcast {podcast_id}: {str(e)}")
        raise
    finally:
        conn.close()


def cleanup_failed_podcast(podcast_id: str) -> None:
    """
    Delete partial files for failed podcasts.
    
    This removes:
    - Audio file (.mp3)
    - Script file (_script.json)
    - Database entry
    
    Args:
        podcast_id: Unique podcast identifier
    """
    try:
        audio_path = PODCAST_DIR / f"{podcast_id}.mp3"
        if audio_path.exists():
            os.remove(audio_path)
            logger.info(f"Deleted audio file: {audio_path}")
        
        script_path = PODCAST_DIR / f"{podcast_id}_script.json"
        if script_path.exists():
            os.remove(script_path)
            logger.info(f"Deleted script file: {script_path}")
        
        delete_podcast(podcast_id)
        
        logger.info(f"Cleanup complete for failed podcast {podcast_id}")
    except Exception as e:
        logger.error(f"Failed to cleanup podcast {podcast_id}: {str(e)}")
        raise


init_database()