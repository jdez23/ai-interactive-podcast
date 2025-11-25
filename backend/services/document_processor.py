"""
Service for processing uploaded documents.

This module handles:
- PDF text extraction
- Text chunking
- Embedding generation
- Storage in vector database
"""

from pathlib import Path
from typing import List

import PyPDF2 
from langchain.text_splitter import RecursiveCharacterTextSplitter 
from database.vector_store import store_document_chunks 
from config.settings import CHUNK_SIZE, CHUNK_OVERLAP

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

async def process_document(document_id: str, file_path: Path) -> int:
    """
    Process a document: extract text, chunk, embed, and store.
    
    TODO - Backend Engineer Tasks:
    1. Call extract_text_from_pdf()
    2. Validate text is not empty
    3. Call chunk_text()
    4. Call database.vector_store.store_document_chunks()
    5. Return number of chunks created
    
    Args:
        document_id: Unique identifier for the document
        file_path: Path to the uploaded PDF
        
    Returns:
        Number of chunks created
        
    Raises:
        ValueError: If document is empty or processing fails
        
    This is the Main Function that ties everything together.
    Called by api/routes/documents.py after file upload.
    """
    text = extract_text_from_pdf(file_path)
    if not text or len(text) < 100: 
        raise ValueError("Document too short")
    chunks = chunk_text(text)
    await store_document_chunks(document_id, chunks)
    return len(chunks)