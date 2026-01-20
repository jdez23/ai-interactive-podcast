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

### 6. `test_audio.py`
Tests the ElevenLabs audio generation service:
- Text-to-speech conversion with host and guest voices
- Audio quality verification
- Long text handling
- Special character support (quotes, symbols, emojis, numbers)
- Error handling (empty text, invalid voice IDs)
- Cohesive podcast-style dialogue about Mars

**Run:**
```bash
cd backend
source venv/bin/activate
python tests/test_audio.py
```

**Expected Output:**
- Generates 4 MP3 files in `backend/generated/podcasts/`:
  - `test_host.mp3` - Host introduction
  - `test_guest.mp3` - Guest response
  - `test_long.mp3` - Detailed Mars facts
  - `test_special.mp3` - Mars life potential with special characters

### 7. `test_openai_with_pdfs.py`
Tests OpenAI service with real PDF documents:
- PDF text extraction and chunking
- Podcast dialogue generation from document content
- Host/guest conversation formatting
- Token usage tracking and cost estimation
- Error handling for API failures
- Interactive and command-line modes

**Run (Interactive Mode):**
```bash
cd backend
source venv/bin/activate
python tests/test_openai_with_pdfs.py
# Then enter your PDF path when prompted
```

**Run (Command Line Mode):**
```bash
cd backend
source venv/bin/activate
python tests/test_openai_with_pdfs.py /path/to/your/file.pdf "Your Topic"
```

**Examples:**
```bash
# With custom topic
python tests/test_openai_with_pdfs.py ~/Desktop/research.pdf "Machine Learning"

# Without topic (uses filename)
python tests/test_openai_with_pdfs.py ~/Desktop/biology_notes.pdf
```

**Expected Output:**
- Extracts text from your PDF
- Creates chunks from the content
- Generates 3-minute podcast dialogue with Host A and Host B
- Shows token usage and cost estimate (~$0.001-0.003 per test)
- Displays full generated dialogue

### 8. `test_script_generator.py`
Tests the podcast script generation pipeline:
- Script generation from document chunks
- Multiple target lengths (short ~3min, medium ~5min, long ~10min)
- Natural host/guest dialogue formatting
- Speaker alternation and quality validation
- Token management and content summarization
- Error handling for missing documents
- Structure validation

**Run (Comprehensive Test):**
```bash
cd backend
source venv/bin/activate
python tests/test_script_generator.py /path/to/your/file.pdf
```

**Run (Quick Test):**
```bash
cd backend
source venv/bin/activate
python tests/run_script_test.py /path/to/your/file.pdf short
```

**Examples:**
```bash
# Test all three lengths (short, medium, long)
python tests/test_script_generator.py ~/Desktop/article.pdf

# Quick test with short script
python tests/run_script_test.py ~/Desktop/article.pdf short

# Test medium length
python tests/run_script_test.py ~/Desktop/research.pdf medium

# Test long script
python tests/run_script_test.py ~/Desktop/book_chapter.pdf long
```

**Expected Output:**
- Processes document and stores chunks
- Generates structured podcast script with host/guest dialogue
- Shows quality metrics (word count, speaker balance, alternation rate)
- Displays complete script with all exchanges
- Validates script structure and format
- Tests all three target lengths sequentially

### 9. `test_full_pipeline.py`
Tests the complete podcast generation API pipeline end-to-end:
- PDF upload via API endpoint
- Podcast generation from uploaded document
- Background task processing and status tracking
- Audio file generation and verification
- Script file generation and validation
- Complete workflow from upload to playable podcast

**Run:**
```bash
cd backend
source venv/bin/activate
python tests/test_full_pipeline.py /path/to/your/file.pdf short
```

**Examples:**
```bash
python tests/test_full_pipeline.py ~/Desktop/article.pdf short

python tests/test_full_pipeline.py ~/Desktop/research.pdf medium

python tests/test_full_pipeline.py ~/Desktop/book.pdf long
```

**Expected Output:**
- Uploads document and receives document_id
- Initiates podcast generation and receives podcast_id
- Polls status every 5 seconds until complete
- Verifies audio file exists (MP3 format, reasonable size)
- Verifies script file exists (JSON format with exchanges)
- Validates duration matches target length
- Complete test takes 1-3 minutes depending on podcast length

### 10. `manual_podcast_test.py`
Interactive script for manual testing of podcast generation API:
- Prompts for document_id and target duration
- Calls POST /api/podcasts/generate endpoint
- Polls GET /api/podcasts/{id} for status updates
- Displays real-time progress and final results
- Shows audio URL for playback

**Run:**
```bash
cd backend
source venv/bin/activate
python tests/manual_podcast_test.py
```

**Expected Output:**
- Interactive prompts for input
- Real-time status updates (processing → complete)
- Stage information (generating_script, generating_audio, concatenating_audio)
- Final podcast details with audio URL
- Access link to generated MP3 file

### 11. `test_podcast_generation.py`
Automated API endpoint tests for podcast generation:
- POST /api/podcasts/generate validation
- GET /api/podcasts/{id} status checking
- GET /api/podcasts/ list endpoint
- Error handling (invalid document_id, invalid duration)
- 404 responses for non-existent podcasts
- Response format validation

**Run:**
```bash
cd backend
source venv/bin/activate
python tests/test_podcast_generation.py
```

**Expected Output:**
- Tests invalid document_id returns 400
- Tests invalid target_duration returns 400
- Tests non-existent podcast_id returns 404
- Tests list endpoint returns all podcasts
- All validation tests pass

### 12. `test_podcast_storage.py`
Tests the podcast storage layer (SQLite database):
- Save and retrieve podcast metadata
- Status progression (processing → complete → failed)
- Update multiple fields at once
- List all podcasts
- Podcast not found handling
- Database persistence

**Run:**
```bash
cd backend
source venv/bin/activate
python tests/test_podcast_storage.py
```

**Expected Output:**
- Creates test podcasts in database
- Verifies save/retrieve operations
- Tests status transitions
- Validates all database fields
- Cleans up test data automatically
- All tests pass (~6 tests)

**Note:** This test only validates the database storage layer. No actual audio files are generated or required.

### 13. `test_qa_context_simple.py`
Tests the Q&A context builder service:
- Error handling (empty inputs, invalid podcast_id, negative timestamp)
- Dialogue extraction at different timestamps (beginning, middle, end, beyond)
- Context validation (required fields, correct types)
- Timestamp estimation algorithm
- Recent dialogue lookback window

**Run:**
```bash
cd backend
source venv/bin/activate
python tests/test_qa_context_simple.py
```

**Expected Output:**
- All error handling tests pass (4 tests)
- Dialogue extraction works at various timestamps (5 tests)
- Context validation passes (3 tests)
- Total: 3/3 test suites passed
- Exit code: 0

**Note:** This is an automated test that doesn't require a real podcast. It tests the core logic with mock data.

### 14. `test_qa_context_builder.py`
Interactive tests for Q&A context builder with real podcasts:
- Basic context building with actual podcast data
- Document chunk retrieval via semantic search
- Recent dialogue extraction based on playback position
- Different question types and timestamp edge cases
- End-to-end context validation

**Run:**
```bash
cd backend
source venv/bin/activate
python tests/test_qa_context_builder.py
```

**Prerequisites:**
- At least one completed podcast in the database
- Podcast must have associated script file ({podcast_id}_script.json)
- Source documents must be in vector database

**Expected Output:**
- Prompts for podcast_id for interactive tests
- Shows retrieved document chunks with relevance scores
- Displays recent dialogue with estimated timestamps
- Validates complete context structure
- Tests various timestamp positions and question types

**Note:** This test requires user input and a real podcast. Use `test_qa_context_simple.py` for automated testing.

### 15. `test_podcast_api_integration.py`
Integration tests for podcast API endpoints:
- Health check endpoint
- Document upload (optional if test file exists)
- Podcast generation initiation
- Status polling and tracking
- List all podcasts endpoint
- 404 error handling

**Prerequisites:**
- Backend server must be running (`python main.py`)
- Optional: Test PDF file in `backend/uploads/test.pdf`

**Run:**
```bash
# Terminal 1: Start server
cd backend
source venv/bin/activate
python main.py

# Terminal 2: Run tests
cd backend
source venv/bin/activate
python tests/test_podcast_api_integration.py
```

**Expected Output:**
- Server health check passes
- Document upload works (if test file exists)
- Podcast generation starts successfully
- Status endpoint returns correct data
- List endpoint shows all podcasts
- 404 handling works correctly

## Running All Tests

### Unit Tests (No Server Required)

To run all unit tests sequentially:

```bash
cd backend
source venv/bin/activate
python tests/test_vector_store.py && \
python tests/test_storage_errors.py && \
python tests/test_end_to_end.py && \
python tests/test_retrieve_chunks.py && \
python tests/test_audio.py && \
python tests/test_podcast_storage.py && \
python tests/test_qa_context_simple.py
```

### Integration Tests (Server Required)

To run integration tests (requires running server):

```bash
# Terminal 1: Start server
cd backend
source venv/bin/activate
python main.py

# Terminal 2: Run integration tests
cd backend
source venv/bin/activate
python tests/test_podcast_api_integration.py
```

**Note:** The following tests require a PDF file path and are run separately with your own documents:
- `test_openai_with_pdfs.py` - OpenAI script generation test
- `test_script_generator.py` - Script generator pipeline test
- `test_full_pipeline.py` - Complete podcast generation test (upload + generate)

**Example:**
```bash
python tests/test_full_pipeline.py ~/Desktop/your-document.pdf short
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

9. **ElevenLabs text-to-speech integration**
   - ✅ Two distinct voices configured (host and guest)
   - ✅ Successfully converts text to speech with error handling
   - ✅ Audio quality verified and saved to correct directory

10. **OpenAI service for podcast script generation**
    - ✅ OpenAI client configured with API key and timeout
    - ✅ Prompt templates for host/guest dialogue generation
    - ✅ Error handling for API failures (invalid key, rate limits, network errors)
    - ✅ Retry logic with exponential backoff
    - ✅ Token usage tracking for cost monitoring
    - ✅ Tested with real PDF documents (3+ different topics)

11. **Script generator pipeline (generate_podcast_script)**
    - ✅ Takes document chunks and generates natural dialogue
    - ✅ Output formatted as alternating host/guest exchanges
    - ✅ Each exchange has speaker label ("host" or "guest") and text
    - ✅ Script flows naturally (engaging, not robotic)
    - ✅ Tested with short content (1-2 chunks)
    - ✅ Tested with longer content (10+ chunks)
    - ✅ Different content types work (technical, narrative, etc.)
    - ✅ Multiple target lengths supported (short, medium, long)
    - ✅ Quality validation (speaker alternation, natural reactions, questions)

12. **Podcast storage and retrieval system**
    - ✅ Podcast metadata storage implemented (SQLite)
    - ✅ GET /api/podcasts/{id} endpoint created
    - ✅ Returns podcast details (status, audio_url, metadata)
    - ✅ Status tracking works (processing, complete, failed)
    - ✅ Audio file paths stored correctly
    - ✅ Failed generation cleanup implemented
    - ✅ GET /api/podcasts endpoint (list all podcasts)
    - ✅ Tested with multiple podcasts
    - ✅ Database persists across server restarts
    - ✅ Concurrent podcast generation supported

13. **Q&A Context Builder (build_qa_context)**
    - ✅ Function exists in `services/qa_context_builder.py`
    - ✅ Accepts podcast_id, question, timestamp parameters
    - ✅ Returns dictionary with required fields (question, timestamp, document_chunks, recent_dialogue, podcast_metadata)
    - ✅ Retrieves podcast metadata from database
    - ✅ Searches document chunks using semantic search (top 5 relevant chunks)
    - ✅ Loads podcast script from JSON file
    - ✅ Extracts recent dialogue based on timestamp (60-second lookback window)
    - ✅ Includes estimated timestamps for dialogue exchanges
    - ✅ Error handling for podcast not found, empty question, invalid timestamp, missing script file
    - ✅ Comprehensive logging throughout
    - ✅ Tested with 3+ different scenarios (error cases, dialogue extraction, validation)
    - ✅ Works with mock data and ready for real podcast integration

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