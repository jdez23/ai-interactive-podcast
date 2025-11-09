"""
API routes for document upload and management.

This module handles PDF document uploads and processing.
Backend engineer should implement the actual upload and processing logic.
"""

from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import uuid

router = APIRouter()


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """
    Upload a PDF document for processing.
    
    TODO - Backend Engineer Tasks:
    1. Validate file type (must be PDF)
    2. Generate unique document_id
    3. Save file to uploads directory
    4. Call document_processor.process_document()
    5. Return document metadata
    
    Args:
        file: Uploaded PDF file
        
    Returns:
        {
            "document_id": "doc_abc123",
            "filename": "example.pdf",
            "status": "processed",
            "chunks_count": 42
        }
        
    Raises:
        HTTPException: If file is not PDF or processing fails
        
    See Also:
        - services/document_processor.py for processing logic
        - config/settings.py for UPLOAD_DIR path
    """
    # TODO: Implement document upload
    # Hints:
    # - Check file.filename.endswith('.pdf')
    # - Use uuid to generate document_id
    # - Save file to config.settings.UPLOAD_DIR
    # - Call await process_document(document_id, file_path)
    
    # STUB: Return placeholder response
    return {
        "document_id": "doc_stub_123",
        "filename": file.filename,
        "status": "stub_implementation",
        "chunks_count": 0,
        "message": "TODO: Implement actual document processing"
    }


@router.get("/list")
async def list_documents():
    """
    List all uploaded documents.
    
    TODO - Backend Engineer Tasks:
    1. Scan uploads directory for PDF files
    2. Return list of document metadata
    
    Returns:
        {
            "documents": [
                {"document_id": "doc_123", "filename": "example.pdf", "size_bytes": 12345},
                ...
            ]
        }
    """
    # TODO: Implement document listing
    
    # STUB: Return empty list
    return {
        "documents": [],
        "message": "TODO: Implement document listing"
    }


@router.get("/{document_id}")
async def get_document(document_id: str):
    """
    Get metadata for a specific document.
    
    TODO - Backend Engineer Tasks:
    1. Look up document by ID
    2. Return document metadata
    3. Raise 404 if not found
    
    Args:
        document_id: Unique document identifier
        
    Returns:
        Document metadata
        
    Raises:
        HTTPException: 404 if document not found
    """
    # TODO: Implement document retrieval
    
    # STUB: Return placeholder
    return {
        "document_id": document_id,
        "status": "stub_implementation",
        "message": "TODO: Implement document retrieval"
    }