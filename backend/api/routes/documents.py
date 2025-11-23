"""
API routes for document upload and management.

This module handles PDF document uploads and processing.
Backend engineer should implement the actual upload and processing logic.
"""

from services.document_processor import process_document
from config.settings import UPLOAD_DIR
from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import uuid

router = APIRouter()


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """
    Upload a PDF document for processing.
    
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
    """
    # Validate file type
    if not file.filename.endswith('.pdf'):
        raise HTTPException(
            status_code=400, 
            detail="Only PDF files are allowed"
        )
    
    try:
        # Generate unique document ID
        document_id = f"doc_{uuid.uuid4().hex[:12]}"
        file_path = UPLOAD_DIR / f"{document_id}.pdf"
        
        # Save uploaded file
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)
        
        # Process document
        chunks_count = await process_document(document_id, file_path)
        
        return {
            "document_id": document_id,
            "filename": file.filename,
            "status": "processed",
            "chunks_count": chunks_count,
        }
        
    except ValueError as e:
        # Document processing errors (e.g., "Document too short")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Unexpected errors
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to process document: {str(e)}"
        )



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