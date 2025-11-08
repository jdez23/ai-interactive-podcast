# API Specification

Base URL: `http://localhost:8000` (development)

## Endpoints

### Health Check

**GET /**
```json
{
  "message": "AI Interactive Podcast API",
  "status": "healthy",
  "version": "1.0.0"
}
```

### Document Upload

**POST /api/documents/upload**

Upload a PDF document for processing.

**Request:**
- Content-Type: `multipart/form-data`
- Body: `file` (PDF file)

**Response:**
```json
{
  "document_id": "doc_abc123",
  "filename": "american_revolution.pdf",
  "status": "processed",
  "chunks_count": 42
}
```

**Status Codes:**
- 200: Success
- 400: Invalid file type (not PDF)
- 500: Processing error

---

### Generate Podcast

**POST /api/podcasts/generate**

Generate a podcast from uploaded documents.

**Request:**
```json
{
  "document_ids": ["doc_abc123", "doc_def456"],
  "topic": "The American Revolution",
  "duration_minutes": 3
}
```

**Response:**
```json
{
  "podcast_id": "podcast_xyz789",
  "audio_url": "http://localhost:8000/generated/podcasts/podcast_xyz789.mp3",
  "script": "Host A: Welcome to today's session...",
  "duration_seconds": 180
}
```

**Status Codes:**
- 200: Success
- 404: Document ID not found
- 500: Generation error

---

### Ask Question

**POST /api/questions/ask**

Ask a question during podcast playback.

**Request:**
```json
{
  "podcast_id": "podcast_xyz789",
  "question": "What role did France play in the American Revolution?"
}
```

**Response:**
```json
{
  "answer_audio_url": "http://localhost:8000/generated/answers/answer_123.mp3",
  "answer_text": "France played a crucial role by providing military support...",
  "sources": ["doc_abc123"],
  "used_web_search": false
}
```

**Status Codes:**
- 200: Success
- 404: Podcast ID not found
- 500: Answer generation error

---

## Error Response Format

All errors follow this format:
```json
{
  "detail": "Error message describing what went wrong"
}
```

## Rate Limits

Development server has no rate limits. Production would implement:
- Document upload: 10 per hour
- Podcast generation: 5 per hour
- Questions: 30 per hour

## Authentication

Not implemented for demo. Production would use:
- Apple ID OAuth
- JWT tokens
- API key for service-to-service
