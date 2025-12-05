# Test Suite for Document Storage Pipeline

This directory contains comprehensive tests for the document processing and storage pipeline.

## Test Files

### 1. `test_vector_store.py`
Tests core vector store functionality:
- Adding chunks to ChromaDB
- Semantic search queries
- Retrieving chunks for specific documents
- Database persistence
- Multiple document handling

**Run:**
```bash
cd backend
source venv/bin/activate 
python tests/test_vector_store.py
```

### 2. `test_storage_errors.py`
Tests error handling:
- Empty chunks handling
- Chroma connection errors
- Error propagation through the pipeline
- Logging of errors

**Run:**
```bash
cd backend
python tests/test_storage_errors.py
```

### 3. `test_end_to_end.py`
Tests the complete pipeline:
- PDF upload and storage
- Text extraction
- Text chunking
- Vector storage with metadata
- Semantic search
- Multiple document handling

**Run:**
```bash
cd backend
source venv/bin/activate 
python tests/test_end_to_end.py
```

### 4. `test_document_processor.py`
Unit tests for document processing functions (existing file).

### 5. `test_retrieve_chunks.py`
Tests the `retrieve_relevant_chunks()` function for semantic search:
- Basic semantic search with multiple queries
- Document ID filtering (single and multiple documents)
- n_results parameter validation
- Metadata structure verification
- Edge cases (empty queries, non-existent documents)
- Relevance ranking verification

**Run:**
```bash
cd backend
source venv/bin/activate
python tests/test_retrieve_chunks.py
```

## Running All Tests

To run all tests sequentially:

```bash
cd backend
source venv/bin/activate
python tests/test_vector_store.py && \
python tests/test_storage_errors.py && \
python tests/test_end_to_end.py && \
python tests/test_retrieve_chunks.py
```

## What's Being Tested

### ✅ Acceptance Criteria Coverage

1. **store_document_chunks() function implemented**
   - ✅ Function exists in `database/vector_store.py`
   - ✅ Accepts document_id, chunks, and source parameters
   - ✅ Returns status dict with success/failure

2. **Chunks stored in Chroma with metadata**
   - ✅ document_id
   - ✅ chunk_index
   - ✅ source (filename)
   - ✅ timestamp (ISO 8601 format)

3. **process_document() calls storage after chunking**
   - ✅ Full pipeline: extract → chunk → store
   - ✅ Passes source filename to storage
   - ✅ Returns result with chunks_count

4. **Full pipeline tested end-to-end via upload endpoint**
   - ✅ Upload endpoint works
   - ✅ Documents processed successfully
   - ✅ Chunks retrievable from Chroma

5. **Error handling for storage failures**
   - ✅ Catches Chroma connection errors
   - ✅ Returns failed status on error
   - ✅ Propagates errors to caller

6. **Multiple documents can be stored without ID conflicts**
   - ✅ Unique chunk IDs: `{document_id}_chunk_{index}`
   - ✅ Multiple documents tested
   - ✅ No ID conflicts

7. **Logs show storage activity**
   - ✅ Logs chunks stored
   - ✅ Logs errors
   - ✅ Logs document processing steps

8. **retrieve_relevant_chunks() function implemented**
   - ✅ Semantic search with document_id filtering
   - ✅ Configurable n_results parameter
   - ✅ Returns chunks with metadata, tested with 3+ queries

## Expected Output

All tests should pass with output similar to:

```
============================================================
TESTING CHROMADB VECTOR STORE
============================================================

Test 1: Adding sample chunks to database...
------------------------------------------------------------
✅ Successfully added chunks to collection
   Status: success
   Chunks stored: 3
   ...

✨ ALL TESTS PASSED SUCCESSFULLY!
```

## Troubleshooting

### Issue: "Metadata should include source"
**Solution:** Clear old test data from the database:
```python
collection.delete(where={"document_id": {"$in": ["test_doc_1", "test_doc_2"]}})
```

### Issue: "Connection refused"
**Solution:** Ensure OpenAI API key is set in `.env` file:
```
OPENAI_API_KEY=your_key_here
```

### Issue: Import errors
**Solution:** Ensure you're in the backend directory and have activated the virtual environment:
```bash
cd backend
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
```

## Manual Testing with Upload Endpoint

To test the upload endpoint manually:

1. Start the server:
```bash
cd backend
uvicorn main:app --reload
```

2. Upload a PDF:
```bash
curl -X POST "http://localhost:8000/api/documents/upload" \
  -F "file=@path/to/your/document.pdf"
```

3. Check the response:
```json
{
  "document_id": "doc_abc123",
  "filename": "document.pdf",
  "status": "processed",
  "chunks_count": 42
}
```

4. Verify in logs:
```
INFO:database.vector_store:Successfully stored 42 chunks for document doc_abc123 (source: doc_abc123.pdf)
```

## Next Steps

After all tests pass:
1. Test with real PDF documents
2. Verify chunks are searchable
3. Test error scenarios (corrupt PDFs, network issues)
4. Monitor logs for any issues
5. Deploy to production