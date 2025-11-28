"""
End-to-end test for document upload pipeline.

Tests the complete flow:
1. Upload PDF → 2. Extract text → 3. Chunk → 4. Store in Chroma
"""

import asyncio
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from services.document_processor import process_document, extract_text_from_pdf, chunk_text
from database.vector_store import collection, search_documents


async def test_end_to_end_pipeline():
    """Test the complete document processing pipeline."""
    
    print("=" * 60)
    print("END-TO-END PIPELINE TEST")
    print("=" * 60)
    
    print("\nStep 1: Creating test PDF...")
    print("-" * 60)
    
    test_pdf_path = Path(__file__).parent.parent / "uploads" / "test_e2e.pdf"
    test_pdf_path.parent.mkdir(exist_ok=True)
    
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        
        c = canvas.Canvas(str(test_pdf_path), pagesize=letter)
        c.drawString(100, 750, "Machine Learning Fundamentals")
        c.drawString(100, 730, "")
        c.drawString(100, 710, "Machine learning is a subset of artificial intelligence that")
        c.drawString(100, 690, "enables computers to learn from data without being explicitly")
        c.drawString(100, 670, "programmed. It uses algorithms to identify patterns in data")
        c.drawString(100, 650, "and make predictions or decisions based on those patterns.")
        c.drawString(100, 630, "")
        c.drawString(100, 610, "Neural networks are computational models inspired by the")
        c.drawString(100, 590, "structure and function of biological neural networks in the")
        c.drawString(100, 570, "human brain. They consist of interconnected nodes (neurons)")
        c.drawString(100, 550, "that process and transmit information.")
        c.save()
        print(f"   ✅ Created test PDF at: {test_pdf_path}")
    except ImportError:
        print("   ⚠️  reportlab not installed, using minimal PDF")
        with open(test_pdf_path, "wb") as f:
            f.write(b"%PDF-1.4\n")
            f.write(b"1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n")
            f.write(b"2 0 obj<</Type/Pages/Count 1/Kids[3 0 R]>>endobj\n")
            f.write(b"3 0 obj<</Type/Page/MediaBox[0 0 612 792]/Parent 2 0 R/Resources<<>>>>endobj\n")
            f.write(b"xref\n0 4\n0000000000 65535 f\n0000000009 00000 n\n")
            f.write(b"0000000058 00000 n\n0000000115 00000 n\n")
            f.write(b"trailer<</Size 4/Root 1 0 R>>\nstartxref\n203\n%%EOF\n")
    
    print("\nStep 2: Extracting text from PDF...")
    print("-" * 60)
    try:
        text = extract_text_from_pdf(test_pdf_path)
        print(f"   ✅ Extracted {len(text)} characters")
        print(f"   Preview: {text[:100]}...")
    except Exception as e:
        print(f"   ❌ Error extracting text: {e}")
        return False
    
    print("\nStep 3: Chunking text...")
    print("-" * 60)
    try:
        chunks = chunk_text(text)
        print(f"   ✅ Created {len(chunks)} chunks")
        for i, chunk in enumerate(chunks[:2], 1):
            print(f"   Chunk {i}: {chunk[:60]}...")
    except Exception as e:
        print(f"   ❌ Error chunking text: {e}")
        return False
    
    print("\nStep 4: Running full pipeline with process_document()...")
    print("-" * 60)
    try:
        document_id = "test_e2e_doc"
        result = await process_document(document_id, test_pdf_path)
        
        print(f"   ✅ Pipeline completed successfully!")
        print(f"   Status: {result['status']}")
        print(f"   Chunks stored: {result['chunks_count']}")
        
        assert result['status'] == 'success', "Pipeline should succeed"
        assert result['chunks_count'] > 0, "Should create at least one chunk"
        
    except Exception as e:
        print(f"   ❌ Error in pipeline: {e}")
        return False
    
    print("\nStep 5: Verifying chunks in Chroma...")
    print("-" * 60)
    try:
        results = await search_documents("machine learning", document_ids=[document_id], n_results=5)
        
        print(f"   ✅ Found {len(results['chunks'])} chunks in database")
        
        for i, (chunk, metadata) in enumerate(zip(results['chunks'], results['metadatas']), 1):
            print(f"\n   Chunk {i}:")
            print(f"      Document ID: {metadata.get('document_id')}")
            print(f"      Chunk Index: {metadata.get('chunk_index')}")
            print(f"      Source: {metadata.get('source')}")
            print(f"      Timestamp: {metadata.get('timestamp')}")
            print(f"      Content: {chunk[:80]}...")
            
            assert metadata.get('document_id') == document_id, "Document ID should match"
            assert 'chunk_index' in metadata, "Should have chunk_index"
            assert 'source' in metadata, "Should have source"
            assert 'timestamp' in metadata, "Should have timestamp"
        
        print(f"\n   ✅ All metadata fields verified!")
        
    except Exception as e:
        print(f"   ❌ Error verifying storage: {e}")
        return False
    
    print("\nStep 6: Testing multiple document storage...")
    print("-" * 60)
    try:
        document_id_2 = "test_e2e_doc_2"
        result2 = await process_document(document_id_2, test_pdf_path)
        
        print(f"   ✅ Second document processed: {result2['chunks_count']} chunks")
        
        total_count = collection.count()
        print(f"   Total chunks in database: {total_count}")
        
        all_results = await search_documents("machine learning", n_results=10)
        doc_ids = set(m['document_id'] for m in all_results['metadatas'])
        
        print(f"   Found chunks from {len(doc_ids)} unique documents")
        assert document_id in doc_ids or document_id_2 in doc_ids, "Should find our test documents"
        
    except Exception as e:
        print(f"   ❌ Error with multiple documents: {e}")
        return False
    
    print("\nCleaning up test files...")
    print("-" * 60)
    try:
        if test_pdf_path.exists():
            test_pdf_path.unlink()
            print(f"   ✅ Removed test PDF")
    except Exception as e:
        print(f"   ⚠️  Could not remove test file: {e}")
    
    print("\n" + "=" * 60)
    print("✨ END-TO-END PIPELINE TEST PASSED!")
    print("=" * 60)
    print("\nPipeline verified:")
    print("   1. ✅ PDF upload and storage")
    print("   2. ✅ Text extraction")
    print("   3. ✅ Text chunking")
    print("   4. ✅ Vector storage with metadata")
    print("   5. ✅ Semantic search")
    print("   6. ✅ Multiple document handling")
    print("\nThe complete pipeline is working correctly!")
    print("=" * 60)
    
    return True


if __name__ == "__main__":
    success = asyncio.run(test_end_to_end_pipeline())
    sys.exit(0 if success else 1)