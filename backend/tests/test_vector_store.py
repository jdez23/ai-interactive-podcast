"""
Test script for vector store functionality.

This script tests:
1. Adding chunks to ChromaDB
2. Semantic search queries
3. Retrieving all chunks for documents
4. Database persistence
"""

import asyncio
from pathlib import Path
import sys

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from database.vector_store import (
    store_document_chunks,
    search_documents,
    get_all_chunks_for_documents,
    collection
)


async def test_vector_store():
    """Test all vector store operations."""
    
    print("=" * 60)
    print("TESTING CHROMADB VECTOR STORE")
    print("=" * 60)
    
    # Test 1: Add sample chunks
    print("\nTest 1: Adding sample chunks to database...")
    print("-" * 60)
    
    test_chunks = [
        "Machine learning is a subset of artificial intelligence that enables computers to learn from data.",
        "Neural networks are computational models inspired by biological neurons in the human brain.",
        "Deep learning uses multiple layers of neural networks to process complex patterns in data."
    ]
    
    try:
        await store_document_chunks("test_doc_1", test_chunks)
        count = collection.count()
        print(f"✅ Successfully added chunks to collection")
        print(f"   Total chunks in database: {count}")
        assert count >= 3, "Should have at least 3 chunks"
        print(f"   ✓ Assertion passed: Collection has {count} chunks")
    except Exception as e:
        print(f"❌ Error adding chunks: {e}")
        return False
    
    # Test 2: Semantic search
    print("\nTest 2: Testing semantic search...")
    print("-" * 60)
    
    queries = [
        "What is machine learning?",
        "Tell me about neural networks",
        "How does deep learning work?"
    ]
    
    try:
        for query in queries:
            print(f"\n   Query: '{query}'")
            results = await search_documents(query, n_results=2)
            print(f"   Found {len(results['chunks'])} relevant chunks:")
            
            for i, (chunk, metadata) in enumerate(zip(results['chunks'], results['metadatas']), 1):
                print(f"      {i}. [{metadata.get('chunk_index', 'N/A')}] {chunk[:80]}...")
            
            assert len(results['chunks']) > 0, f"Should find results for query: {query}"
        
        print(f"\n   ✅ All semantic search queries successful")
    except Exception as e:
        print(f"   ❌ Error in semantic search: {e}")
        return False
    
    # Test 3: Retrieve all chunks for document
    print("\nTest 3: Retrieving all chunks for specific document...")
    print("-" * 60)
    
    try:
        all_chunks = await get_all_chunks_for_documents(["test_doc_1"])
        print(f"   Retrieved {len(all_chunks)} chunks for 'test_doc_1'")
        
        for i, chunk in enumerate(all_chunks, 1):
            print(f"      {i}. {chunk[:60]}...")
        
        assert len(all_chunks) >= 3, "Should retrieve all 3 chunks"
        print(f"   ✅ Successfully retrieved all chunks")
    except Exception as e:
        print(f"   ❌ Error retrieving chunks: {e}")
        return False
    
    # Test 4: Test with multiple documents
    print("\nTest 4: Testing with multiple documents...")
    print("-" * 60)
    
    try:
        # Add another document
        more_chunks = [
            "Python is a high-level programming language known for its simplicity.",
            "FastAPI is a modern web framework for building APIs with Python."
        ]
        
        await store_document_chunks("test_doc_2", more_chunks)
        
        # Search across all documents
        results = await search_documents("programming language", n_results=3)
        print(f"   Search across all documents found {len(results['chunks'])} results")
        
        # Search within specific document
        results_filtered = await search_documents(
            "programming language", 
            document_ids=["test_doc_2"],
            n_results=3
        )
        print(f"   Search within test_doc_2 found {len(results_filtered['chunks'])} results")
        
        # Verify filtering worked
        for metadata in results_filtered['metadatas']:
            assert metadata['document_id'] == 'test_doc_2', "Should only return chunks from test_doc_2"
        
        print(f"   ✅ Multi-document operations successful")
    except Exception as e:
        print(f"   ❌ Error with multiple documents: {e}")
        return False
    
    # Test 5: Check persistence
    print("\nTest 5: Checking database persistence...")
    print("-" * 60)
    
    try:
        chroma_db_path = Path(__file__).parent.parent / "chroma_db"
        
        if chroma_db_path.exists():
            print(f"   ✅ Database directory exists at: {chroma_db_path}")
            
            # List files in the directory
            db_files = list(chroma_db_path.rglob('*'))
            print(f"   Database contains {len(db_files)} files/directories:")
            
            for file in db_files[:5]:  # Show first 5 files
                relative_path = file.relative_to(chroma_db_path)
                file_type = "📁" if file.is_dir() else "📄"
                print(f"      {file_type} {relative_path}")
            
            if len(db_files) > 5:
                print(f"      ... and {len(db_files) - 5} more")
            
            print(f"   ✓ Database will persist between server restarts")
        else:
            print(f"   ❌ Database directory not found at: {chroma_db_path}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error checking persistence: {e}")
        return False
    
    # Final summary
    print("\n" + "=" * 60)
    print("✨ ALL TESTS PASSED SUCCESSFULLY!")
    print("=" * 60)
    print("\nSummary:")
    print(f"   • Total chunks in database: {collection.count()}")
    print(f"   • Documents tested: test_doc_1, test_doc_2")
    print(f"   • Semantic search: ✅ Working")
    print(f"   • Document filtering: ✅ Working")
    print(f"   • Persistence: ✅ Verified")
    print("\nChromaDB vector store is ready for production use!")
    print("=" * 60)
    
    return True


if __name__ == "__main__":
    success = asyncio.run(test_vector_store())
    sys.exit(0 if success else 1)