# AI Interactive Podcast

An AI-powered interactive learning platform that generates podcast-style discussions from documents and enables real-time Q&A during playback.

## Project Structure

This is a monorepo containing:
- **backend/** - Python/FastAPI API server
- **ios/** - SwiftUI iOS application  
- **docs/** - Shared documentation

## Quick Start

### For Backend Engineers
```bash
cd backend
# Follow backend/SETUP.md
```

### For iOS Engineers
```bash
cd ios
# Follow ios/SETUP.md
```

## Team

- **Technical Lead:** Jesse Hernandez
- **Backend Engineer:** Rosario Miller
- **iOS Engineer/UX/UI Designer:** Claudio Trejo
- **Product Managers:** Elian Lopez & Jaime Arias

## Demo Date

**December 1, 2025**

## Project Goals

1. **Upload documents** - Users can upload PDFs about any topic
2. **Generate podcasts** - AI creates conversational 2-3 minute podcasts
3. **Interactive Q&A** - Users can interrupt and ask questions in real-time
4. **Web search fallback** - Questions outside document scope use web search

## Tech Stack

**Backend:**
- Python 3.10+
- FastAPI
- LangChain (RAG)
- Chroma (Vector DB)
- OpenAI GPT-4
- ElevenLabs (TTS)

**iOS:**
- Swift 5.9+
- SwiftUI
- AVFoundation
- Speech Framework

## Documentation

- [Technical Architecture](docs/ARCHITECTURE.md)
- [API Specification](docs/API_SPEC.md)
- [Demo Script](docs/DEMO_SCRIPT.md)

## Development Workflow

1. **Create a branch** for your work: `git checkout -b your-name/feature-name`
2. **Make changes** in your directory (backend/ or ios/)
3. **Commit regularly** with clear messages
4. **Push your branch**: `git push origin your-name/feature-name`
5. **Create Pull Request** for review
6. **Tag [Your Name]** for code review

## Communication

- **Slack:** #apprentice-ai-podcast
- **Daily Standup:** [Time] via Slack
- **Office Hours:** [Your availability]
- **Task Board:** [Linear/Jira link]

## Getting Help

- Check README in your directory (backend/ or ios/)
- Check docs/ folder for architecture and API docs
- Post in Slack channel
- Schedule time with [Your Name]

## License

Internal Apple project - not for public distribution.