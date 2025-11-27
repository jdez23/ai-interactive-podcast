"""
Vector database setup and operations using Chroma.

This manages document storage and semantic search.
"""

from typing import List, Dict

#Import required libraries
import chromadb
from chromadb.utils import embedding_functions
from config.settings import OPENAI_API_KEY, BASE_DIR


#Initialize Chroma client
chroma_client = chromadb.PersistentClient(path=str(BASE_DIR / "chroma_db"))

openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=OPENAI_API_KEY,
    model_name="text-embedding-3-small"
)

collection = chroma_client.get_or_create_collection(
    name="document_chunks",
    embedding_function=openai_ef
)


async def store_document_chunks(document_id: str, chunks: List[str]) -> None:
    """
    Store document chunks in vector database.
    
    Args:
        document_id: Unique identifier for the document
        chunks: List of text chunks to store
        
    What Happens Automatically:
        - Chroma creates embeddings for each chunk using OpenAI
        - Embeddings are vector representations of text meaning
        - These enable semantic search later
        
    Resources:
        - Chroma docs: https://docs.trychroma.com/
        - What are embeddings?: https://platform.openai.com/docs/guides/embeddings
    """
    if not chunks:
        return
    
    # Create unique IDs for each chunk (e.g., "doc_123_chunk_0")
    ids = [f"{document_id}_chunk_{i}" for i in range(len(chunks))]
    
    # Create metadata for each chunk (document_id, chunk_index)
    metadatas = [
        {"document_id": document_id, "chunk_index": i}
        for i in range(len(chunks))
    ]
    
    # Add to collection (embeddings are created automatically by OpenAI)
    collection.add(
        documents=chunks,
        ids=ids,
        metadatas=metadatas
    )


async def search_documents(query: str, document_ids: List[str] = None, n_results: int = 5) -> Dict:
    """
    Search for relevant document chunks using semantic similarity.
    
    Args:
        query: Search query (question or topic)
        document_ids: Optional list of document IDs to search within
        n_results: Number of results to return
        
    Returns:
        {
            "chunks": ["text chunk 1", "text chunk 2", ...],
            "ids": ["doc_123_chunk_5", ...],
            "metadatas": [{"document_id": "doc_123", "chunk_index": 5}, ...]
        }
        
    How Semantic Search Works:
        1. Your query gets converted to an embedding (vector)
        2. Chroma finds chunks with similar embeddings
        3. Similar embeddings = similar meaning
        4. This finds relevant info even if words don't match exactly
        
    Example:
        Query: "What role did France play?"
        Might find: "French military support was crucial..." 
        Even though "France" and "French" are different words!
    """
    # Build where filter if document_ids provided
    where_filter = None
    if document_ids:
        where_filter = {"document_id": {"$in": document_ids}}
    
    # Query the collection with semantic search
    results = collection.query(
        query_texts=[query],
        n_results=n_results,
        where=where_filter
    )
    
    # Return formatted results
    return {
        "chunks": results['documents'][0] if results['documents'] else [],
        "ids": results['ids'][0] if results['ids'] else [],
        "metadatas": results['metadatas'][0] if results['metadatas'] else []
    }


async def get_all_chunks_for_documents(document_ids: List[str]) -> List[str]:
    """
    Retrieve all chunks for specific documents.
    
    Args:
        document_ids: List of document IDs
        
    Returns:
        List of all text chunks from those documents
        
    Use Case:
        When generating podcasts, you might want ALL content
        from selected documents, not just relevant chunks.
    """
    if not document_ids:
        return []
    
    # Query collection with document_id filter to get all matching chunks
    results = collection.get(
        where={"document_id": {"$in": document_ids}}
    )
    
    # Return all matching chunks
    return results['documents'] if results['documents'] else []