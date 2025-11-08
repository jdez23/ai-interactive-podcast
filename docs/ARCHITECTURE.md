# AI Interactive Podcast - Technical Architecture

**Version:** 1.0  
**Date:** November 7, 2025  
**Author:** Jesse Hernandez

---

## 1. Executive Summary

We're building an AI-powered interactive learning experience that generates podcast-style discussions from user documents and allows real-time Q&A during playback. This prototype demonstrates how Apple could integrate conversational AI learning into the Podcasts app ecosystem.

**Core User Flow:**
1. User uploads documents (PDFs, text files) about a topic
2. AI generates a 2-3 minute podcast with two hosts discussing the content
3. User listens and can interrupt to ask questions
4. AI answers using document knowledge or web search
5. Conversation continues naturally

---

## 2. System Architecture
```
┌─────────────────────────────────────────────────────────┐
│                     iOS App (SwiftUI)                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   Upload     │  │    Player    │  │  Interrupt   │  │
│  │   Documents  │  │    Audio     │  │  & Ask       │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└────────────────────┬────────────────────────────────────┘
                     │ REST API (JSON)
                     │
┌────────────────────▼────────────────────────────────────┐
│              Backend API (Python/FastAPI)                │
│  ┌──────────────────────────────────────────────────┐   │
│  │          Document Processing Pipeline            │   │
│  │  PDF Parse → Chunk → Embed → Store in Vector DB │   │
│  └──────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────┐   │
│  │          Podcast Generation Engine               │   │
│  │  Retrieve Docs → LLM Script → Text-to-Speech    │   │
│  └──────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────┐   │
│  │          Question Answering System               │   │
│  │  User Q → Search Docs → Web Search → LLM → TTS  │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
                     │
         ┌───────────┴────────────┐
         │                        │
    ┌────▼─────┐          ┌──────▼──────┐
    │ External │          │   Vector    │
    │   APIs   │          │  Database   │
    │          │          │  (Chroma)   │
    │ • OpenAI │          └─────────────┘
    │ • ElevenLabs│
    │ • Brave   │
    └──────────┘
```

---

## 3. Technology Stack

### Frontend (iOS)
- **SwiftUI** - Native Apple UI framework
- **AVFoundation** - Audio playback
- **Speech Framework** - Voice input (iOS native)
- **URLSession** - API communication

### Backend (Python)
- **FastAPI** - Modern Python web framework
- **LangChain** - RAG (Retrieval Augmented Generation) framework
- **Chroma** - Vector database (runs locally, no cloud setup needed)
- **PyPDF2** - PDF text extraction

### External APIs
- **OpenAI GPT-4 or Anthropic Claude** - Text generation (podcast scripts, Q&A)
- **ElevenLabs** - Text-to-speech (natural voice synthesis)
- **Brave Search API** - Web search for questions outside document scope

---

## 4. API Endpoints

**Base URL:** `http://localhost:8000` (development)

### POST /api/documents/upload
Upload a document for processing.

**Request:**
```json
{
  "file": "<binary PDF data>",
  "filename": "american_revolution.pdf"
}
```

**Response:**
```json
{
  "document_id": "doc_123abc",
  "status": "processing",
  "chunks_count": 42
}
```

---

### POST /api/podcasts/generate
Generate podcast from uploaded documents.

**Request:**
```json
{
  "document_ids": ["doc_123abc", "doc_456def"],
  "topic": "The American Revolution",
  "duration_minutes": 3
}
```

**Response:**
```json
{
  "podcast_id": "podcast_789xyz",
  "audio_url": "http://localhost:8000/generated/podcasts/podcast_789xyz.mp3",
  "script": "Host A: Welcome to today's learning session...",
  "duration_seconds": 180
}
```

---

### POST /api/questions/ask
Ask a question during podcast playback.

**Request:**
```json
{
  "podcast_id": "podcast_789xyz",
  "question": "What role did France play?"
}
```

**Response:**
```json
{
  "answer_audio_url": "http://localhost:8000/generated/answers/answer_123.mp3",
  "answer_text": "France played a crucial role...",
  "sources": ["doc_123abc"],
  "used_web_search": false
}
```

---

## 5. Data Flow

### Flow 1: Document Upload & Processing
1. User selects PDF in iOS app
2. iOS uploads to `/api/documents/upload`
3. Backend extracts text from PDF
4. Text split into chunks (~500 words each)
5. Each chunk converted to embedding (vector representation)
6. Embeddings stored in Chroma vector database
7. Backend returns success to iOS

### Flow 2: Podcast Generation
1. User taps "Generate Podcast" in iOS app
2. iOS calls `/api/podcasts/generate` with document IDs
3. Backend retrieves relevant document chunks
4. LLM generates conversational script between two hosts
5. Script sent to ElevenLabs for voice synthesis
6. Audio file saved and URL returned to iOS
7. iOS downloads and plays audio

### Flow 3: Interactive Q&A
1. User interrupts podcast and asks question
2. iOS captures speech with Speech Framework
3. iOS sends text to `/api/questions/ask`
4. Backend searches vector database for relevant info
5. If found: LLM generates answer from documents
6. If not found: Brave Search API queries web
7. LLM generates natural response
8. Response converted to speech with ElevenLabs
9. iOS plays answer audio, resumes podcast

---

## 6. Key Technical Decisions

**Why Python backend instead of Swift?**
- Richer AI/ML ecosystem (LangChain, vector DBs)
- Faster prototyping for complex logic
- Easier to find resources/examples

**Why Chroma for vector database?**
- Runs locally (no cloud setup required)
- Simple Python API
- Good for prototypes (can migrate to production DB later)

**Why ElevenLabs instead of Apple's text-to-speech?**
- More natural, conversational voices
- Better for podcast-style content
- Apple could acquire/build similar tech for production

**Why FastAPI?**
- Modern, fast Python framework
- Auto-generated API documentation
- Great for beginners (clear error messages)

---

## 7. Demo Scope & Limitations

**What we're building:**
✅ Upload 1-3 PDF documents  
✅ Generate 2-3 minute podcast  
✅ Play audio with basic controls  
✅ Ask 1-2 questions successfully  
✅ Demonstrate web search fallback  

**What we're NOT building (out of scope):**
❌ Multiple file formats (just PDFs)  
❌ User accounts or authentication  
❌ Podcast library or history  
❌ Advanced audio editing  
❌ Production-level error handling  
❌ Deployment to cloud  

---

## 8. Development Environment Setup

**Backend Requirements:**
- Python 3.10+
- pip (Python package manager)
- API keys: OpenAI, ElevenLabs, Brave Search

**iOS Requirements:**
- macOS with Xcode 15+
- iOS 17+ device or simulator
- Apple Developer account (for testing on device)

**Shared:**
- Git/GitHub for version control
- Slack for communication
- Linear/Jira for task tracking

---

## 9. Risk Assessment

| Risk | Impact | Mitigation |
|------|--------|-----------|
| LLM generates poor podcast scripts | High | Extensive prompt engineering, pre-generate backups |
| Voice synthesis sounds robotic | Medium | Choose best ElevenLabs voices, iterate |
| Slow response time (>10s for Q&A) | High | Optimize early, cache common queries |
| API rate limits during demo | Medium | Pre-generate content, use cached responses |
| iOS audio playback issues | Medium | Test extensively on target device |

---

## 10. Success Criteria

**Technical Success:**
- [ ] End-to-end flow works 5 times consecutively
- [ ] Podcast generation < 30 seconds
- [ ] Q&A response < 5 seconds
- [ ] Audio quality is clear and natural

**Demo Success:**
- [ ] Live demo runs smoothly (or recovers gracefully)
- [ ] Audience understands the vision
- [ ] Technical architecture is credible
- [ ] Team presents confidently

---

## 11. Future Enhancements (Post-Demo)

If this moves forward, consider:
- **Apple Intelligence integration** - On-device processing for privacy
- **Multi-modal input** - Images, videos, YouTube links
- **Voice customization** - User chooses host voices/personalities
- **SharePlay integration** - Learn together with friends
- **Siri shortcuts** - "Hey Siri, teach me about [topic]"
- **Podcasts app integration** - Native UI/UX

---

## 12. Learning Resources

**For Backend Engineer:**
- FastAPI Tutorial: https://fastapi.tiangolo.com/tutorial/
- LangChain Docs: https://python.langchain.com/docs/get_started/introduction
- Chroma Quickstart: https://docs.trychroma.com/getting-started

**For Frontend Engineer:**
- SwiftUI Tutorials: https://developer.apple.com/tutorials/swiftui
- AVFoundation Guide: https://developer.apple.com/documentation/avfoundation
- Speech Framework: https://developer.apple.com/documentation/speech

---

## Appendix: Integration with Apple Ecosystem

### Podcasts App Integration (Future)
This feature would naturally integrate into Apple Podcasts as a new "Learn" tab:

**User Journey:**
1. User browses to "Learn" tab in Podcasts app
2. Taps "Create Learning Session"
3. Selects sources from Files, Notes, Safari Reading List, Books
4. AI generates episode, appears in "AI-Generated" section
5. During playback, "Join Conversation" button enables Q&A

**Ecosystem Advantages:**
- Seamless iCloud sync across devices
- SharePlay for group learning
- Siri integration for hands-free operation
- Apple Intelligence for on-device processing
- AirPods spatial audio for immersive experience

---
