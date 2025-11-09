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

# TODO: Import required libraries
# import PyPDF2
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from database.vector_store import store_document_chunks
# from config.settings import CHUNK_SIZE, CHUNK_OVERLAP


def extract_text_from_pdf(pdf_path: Path) -> str:
    """
    Extract text content from a PDF file.
    
    TODO - Backend Engineer Tasks:
    1. Open PDF using PyPDF2.PdfReader
    2. Loop through all pages
    3. Extract text from each page
    4. Combine into single string
    5. Return extracted text
    
    Args:
        pdf_path: Path to PDF file
        
    Returns:
        Extracted text as a single string
        
    Raises:
        ValueError: If PDF is empty or unreadable
        
    Example:
        text = extract_text_from_pdf(Path("document.pdf"))
        
    Resources:
        - PyPDF2 docs: https://pypdf2.readthedocs.io/
    """
    # TODO: Implement PDF text extraction
    # Hints:
    # with open(pdf_path, "rb") as file:
    #     pdf_reader = PyPDF2.PdfReader(file)
    #     for page in pdf_reader.pages:
    #         text += page.extract_text()
    
    raise NotImplementedError("TODO: Implement PDF text extraction")


def chunk_text(text: str, chunk_size: int = 500, chunk_overlap: int = 50) -> List[str]:
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
    # TODO: Implement text chunking
    # Hints:
    # from langchain.text_splitter import RecursiveCharacterTextSplitter
    # splitter = RecursiveCharacterTextSplitter(
    #     chunk_size=chunk_size,
    #     chunk_overlap=chunk_overlap
    # )
    # return splitter.split_text(text)
    
    raise NotImplementedError("TODO: Implement text chunking")


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
    # TODO: Implement complete document processing pipeline
    # Steps:
    # 1. text = extract_text_from_pdf(file_path)
    # 2. if not text or len(text) < 100: raise ValueError("Document too short")
    # 3. chunks = chunk_text(text)
    # 4. await store_document_chunks(document_id, chunks)
    # 5. return len(chunks)
    
    raise NotImplementedError("TODO: Implement document processing pipeline")