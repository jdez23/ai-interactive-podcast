"""
Vector database setup and operations using Chroma.

This manages document storage and semantic search.
"""

from typing import List, Dict

# TODO: Import required libraries
# import chromadb
# from chromadb.utils import embedding_functions
# from config.settings import OPENAI_API_KEY, BASE_DIR


# TODO: Initialize Chroma client
# Hints:
# chroma_client = chromadb.PersistentClient(path=str(BASE_DIR / "chroma_db"))
# 
# openai_ef = embedding_functions.OpenAIEmbeddingFunction(
#     api_key=OPENAI_API_KEY,
#     model_name="text-embedding-ada-002"
# )
#
# collection = chroma_client.get_or_create_collection(
#     name="podcast_documents",
#     embedding_function=openai_ef
# )


async def store_document_chunks(document_id: str, chunks: List[str]) -> None:
    """
    Store document chunks in vector database.
    
    TODO - Backend Engineer Tasks:
    1. Create unique IDs for each chunk (e.g., "doc_123_chunk_0")
    2. Create metadata for each chunk (document_id, chunk_index)
    3. Call collection.add() with chunks, IDs, and metadata
    
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
    # TODO: Implement chunk storage
    # Hints:
    # ids = [f"{document_id}_chunk_{i}" for i in range(len(chunks))]
    # metadatas = [{"document_id": document_id, "chunk_index": i} for i in range(len(chunks))]
    # collection.add(documents=chunks, ids=ids, metadatas=metadatas)
    
    raise NotImplementedError("TODO: Implement chunk storage")


async def search_documents(query: str, document_ids: List[str] = None, n_results: int = 5) -> Dict:
    """
    Search for relevant document chunks using semantic similarity.
    
    TODO - Backend Engineer Tasks:
    1. Build where filter if document_ids provided
    2. Call collection.query() with query text
    3. Return results (chunks, IDs, metadata)
    
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
    # TODO: Implement semantic search
    # Hints:
    # where_filter = {"document_id": {"$in": document_ids}} if document_ids else None
    # results = collection.query(
    #     query_texts=[query],
    #     n_results=n_results,
    #     where=where_filter
    # )
    # return {"chunks": results['documents'][0], "ids": results['ids'][0], ...}
    
    raise NotImplementedError("TODO: Implement semantic search")


async def get_all_chunks_for_documents(document_ids: List[str]) -> List[str]:
    """
    Retrieve all chunks for specific documents.
    
    TODO - Backend Engineer Tasks:
    1. Query collection with document_id filter
    2. Return all matching chunks
    
    Args:
        document_ids: List of document IDs
        
    Returns:
        List of all text chunks from those documents
        
    Use Case:
        When generating podcasts, you might want ALL content
        from selected documents, not just relevant chunks.
    """
    # TODO: Implement full document retrieval
    
    raise NotImplementedError("TODO: Implement full document retrieval")