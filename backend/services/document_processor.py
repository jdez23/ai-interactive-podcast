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
from database.vector_store import store_document_chunks, search_documents
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

async def retrieve_relevant_chunks(
    query: str,
    document_ids: List[str] = None,
    n_results: int = 10
) -> Dict:
    """
    Retrieve relevant document chunks using semantic search.
    
    This function uses the vector database to find chunks that are semantically
    similar to the query, enabling intelligent content retrieval even when
    exact keywords don't match.
    
    Args:
        query: Search query (e.g., "explain neural networks")
        document_ids: Optional list of document IDs to search within
        n_results: Number of chunks to return (default: 10)
        
    Returns:
        {
            "chunks": ["chunk text 1", "chunk text 2", ...],
            "metadatas": [{"document_id": "...", "chunk_index": 0}, ...],
            "relevance_scores": [0.95, 0.87, ...]  # Optional, if available
        }
        
    How Semantic Search Works:
        1. Query gets converted to embedding (vector representation)
        2. Chroma finds chunks with similar embeddings
        3. Similar embeddings = similar meaning
        4. Can find relevant content even if exact words don't match
        
    Example:
        # Basic search
        results = await retrieve_relevant_chunks("machine learning basics", n_results=5)
        
        # Search within specific documents
        results = await retrieve_relevant_chunks(
            "deep learning",
            document_ids=["doc_123", "doc_456"],
            n_results=3
        )
        
    Resources:
        - Chroma Query Docs: https://docs.trychroma.com/reference/Collection#query
        - Vector search explanation: https://www.pinecone.io/learn/vector-search/
    """
    logger.info(f"Retrieving relevant chunks for query: '{query}' (n_results={n_results})")
    
    if not query or not query.strip():
        logger.warning("Empty query provided to retrieve_relevant_chunks")
        return {
            "chunks": [],
            "metadatas": [],
            "relevance_scores": []
        }
    
    try:
        search_result = await search_documents(
            query=query,
            document_ids=document_ids,
            n_results=n_results
        )
        
        if search_result["status"] == "failed":
            error_msg = search_result.get("error", "Unknown error")
            logger.error(f"Search failed: {error_msg}")
            return {
                "chunks": [],
                "metadatas": [],
                "relevance_scores": [],
                "error": error_msg
            }
        
        chunks = search_result.get("chunks", [])
        metadatas = search_result.get("metadatas", [])
        
        logger.info(f"Successfully retrieved {len(chunks)} relevant chunks")
        
        # Note: Chroma doesn't return explicit relevance scores by default
        # The results are already ranked by relevance (most relevant first)
        # We could add distances if needed in the future
        return {
            "chunks": chunks,
            "metadatas": metadatas,
            "relevance_scores": []  # Placeholder for future enhancement
        }
        
    except Exception as e:
        error_msg = f"Error retrieving relevant chunks: {str(e)}"
        logger.error(error_msg)
        return {
            "chunks": [],
            "metadatas": [],
            "relevance_scores": [],
            "error": error_msg
        }