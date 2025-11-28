"""
Service for processing uploaded documents.

This module handles:
- PDF text extraction
- Text chunking
- Embedding generation
- Storage in vector database
"""

from pathlib import Path
from typing import List, Dict
import logging

import PyPDF2
from langchain.text_splitter import RecursiveCharacterTextSplitter
from database.vector_store import store_document_chunks
from config.settings import CHUNK_SIZE, CHUNK_OVERLAP

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_text_from_pdf(pdf_path: Path) -> str:
    """
    Extract text content from a PDF file.
    
    Args:
        pdf_path: Path to PDF file
        
    Returns:
        Extracted text as a single string, or empty string if file is unreadable
        
    Example:
        text = extract_text_from_pdf(Path("document.pdf"))
        
    Resources:
        - PyPDF2 docs: https://pypdf2.readthedocs.io/
    """
    try:
        text = ""
        with open(pdf_path, "rb") as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n\n"

        if not text.strip():
            return ""

        return text.strip()

    except FileNotFoundError:
        return ""
    except Exception as e:
        print(f"Error extracting PDF: {e}")
        return ""

def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, chunk_overlap: int = CHUNK_OVERLAP) -> List[str]:
    """
    Split text into manageable chunks for processing.
    
    TODO - Backend Engineer Tasks:
    1. Create RecursiveCharacterTextSplitter with settings
    2. Split text into chunks
    3. Return list of chunks
    
    Args:
        text: Full document text
        chunk_size: Target size for each chunk (in characters)
        chunk_overlap: Overlap between chunks (in characters)
        
    Returns:
        List of text chunks
        
    Why Chunking?
        - LLMs have token limits
        - Embeddings work better on focused content
        - Easier to find relevant information
        
    Resources:
        - LangChain text splitters: https://python.langchain.com/docs/modules/data_connection/document_transformers/
    """
    if not text or not text.strip():
        return []

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""]
    )
    
    chunks = splitter.split_text(text)
    return chunks

async def process_document(document_id: str, file_path: Path) -> Dict[str, any]:
    """
    Process a document: extract text, chunk, embed, and store.
    
    Args:
        document_id: Unique identifier for the document
        file_path: Path to the uploaded PDF
        
    Returns:
        {
            "chunks_count": int,
            "status": "success" | "failed",
            "error": str (only if failed)
        }
        
    Raises:
        ValueError: If document is empty or processing fails
        
    This is the Main Function that ties everything together.
    Called by api/routes/documents.py after file upload.
    """
    logger.info(f"Processing document {document_id} from {file_path.name}")
    
    text = extract_text_from_pdf(file_path)
    if not text or len(text) < 100:
        logger.error(f"Document {document_id} is too short or empty")
        raise ValueError("Document too short or empty")
    
    logger.info(f"Extracted {len(text)} characters from {file_path.name}")
    
    chunks = chunk_text(text)
    logger.info(f"Created {len(chunks)} chunks from document {document_id}")
    
    storage_result = await store_document_chunks(
        document_id=document_id,
        chunks=chunks,
        source=file_path.name
    )
    
    if storage_result["status"] == "failed":
        error_msg = f"Failed to store document chunks: {storage_result.get('error', 'Unknown error')}"
        logger.error(error_msg)
        raise ValueError(error_msg)
    
    logger.info(f"Successfully processed document {document_id}: {storage_result['chunks_stored']} chunks stored")
    
    return {
        "chunks_count": storage_result["chunks_stored"],
        "status": storage_result["status"]
    }