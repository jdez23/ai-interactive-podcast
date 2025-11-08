# AI Interactive Podcast

An AI-powered interactive learning platform that generates podcast-style discussions from documents and enables real-time Q&A during playback.

**Demo Date:** December 1, 2025

---

## What This Project Does

1. **Upload documents** (PDFs) about any topic you want to learn
2. **AI generates a podcast** with two hosts discussing the content naturally
3. **Listen and interrupt** to ask questions in real-time
4. **Get instant answers** from your documents or web search

Think of it as having a conversation with an AI tutor who has read all your study materials.

---

## Project Structure

This is a monorepo containing both the backend API and iOS app:
```
ai-interactive-podcast/
├── README.md           # You are here
├── docs/               # Shared documentation
│   ├── ARCHITECTURE.md
│   ├── API_SPEC.md
│   └── DEMO_SCRIPT.md
├── backend/            # Python/FastAPI backend
│   └── README.md       # Backend-specific docs
└── ios/                # Swift/SwiftUI iOS app
    └── README.md       # iOS-specific docs
```

---

## Getting Started

### Prerequisites

- **Git** - For cloning the repository
- **Backend:** Python 3.10+, pip
- **iOS:** macOS with Xcode 15+

### Clone the Repository
```bash
# Clone the repo
git clone https://github.com/[your-username]/ai-interactive-podcast.git

# Navigate into the project
cd ai-interactive-podcast
```

### For Backend Engineers
```bash
cd backend
# Follow the setup guide in backend/README.md or backend/SETUP.md
```

Quick start:
1. Create virtual environment: `python3 -m venv venv`
2. Activate it: `source venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Set up `.env` file with API keys
5. Run server: `python main.py`

**Full instructions:** See [backend/SETUP.md](backend/SETUP.md)

### For iOS Engineers
```bash
cd ios
# Follow the setup guide in ios/README.md or ios/SETUP.md
```

Quick start:
1. Open `AIPodcast.xcodeproj` in Xcode
2. Update API base URL in `Constants.swift`
3. Build and run (⌘+R)

**Full instructions:** See [ios/SETUP.md](ios/SETUP.md)

---

## Tech Stack

**Backend:**
- Python 3.10+ with FastAPI
- LangChain for RAG (Retrieval Augmented Generation)
- Chroma vector database
- OpenAI GPT-4 for script generation
- ElevenLabs for voice synthesis
- Brave Search API for web search

**iOS:**
- Swift 5.9+ with SwiftUI
- AVFoundation for audio playback
- Speech Framework for voice input
- Native iOS frameworks

---

## Documentation

- **[Technical Architecture](docs/ARCHITECTURE.md)** - System design and technology decisions
- **[API Specification](docs/API_SPEC.md)** - Complete API documentation
- **[Demo Script](docs/DEMO_SCRIPT.md)** - Demo day preparation and script

---

## Team

- **Technical Lead:** Jesse Hernandez
- **Backend Engineer:** Rosario MIller-Canales
- **iOS Engineer/Designer:** Claudia Trejo
- **Product Managers:** Elian Lopez & Jaime Arias

---

## Project Timeline

- **Kickoff:** November 11, 2024
- **Week 1 (Nov 11-15):** Foundation & design
- **Week 2 (Nov 18-22):** Core build sprint
- **Week 3 (Nov 25-29):** Polish & demo prep
- **Demo Day:** December 1, 2025

---

## Development Workflow

### Branching Strategy
```bash
# Create a branch for your work
git checkout -b your-name/feature-name

# Make changes, commit regularly
git add .
git commit -m "Description of changes"

# Push your branch
git push origin your-name/feature-name

# Create Pull Request on GitHub for review
```

### Daily Standup

- **Time:** [Set time]
- **Format:** What did you do? What will you do? Any blockers?
- **Location:** #apprentice-ai-podcast Slack channel

---

## Project Goals

### Technical Goals
- [ ] End-to-end document → podcast → Q&A flow works
- [ ] Podcast generation completes in <30 seconds
- [ ] Q&A responses in <5 seconds
- [ ] Natural-sounding AI voices
- [ ] Clean, maintainable code

### Demo Goals
- [ ] Live demo runs successfully
- [ ] Audience understands the vision
- [ ] Leadership sees potential
- [ ] Team presents confidently

---

## API Quick Reference

**Base URL:** `http://localhost:8000` (development)

**Endpoints:**
- `POST /api/documents/upload` - Upload PDF document
- `POST /api/podcasts/generate` - Generate podcast from documents
- `POST /api/questions/ask` - Ask question during playback

**Interactive API Docs:** http://localhost:8000/docs (when backend is running)

---

## Troubleshooting

### Backend won't start
- Check virtual environment is activated: `source venv/bin/activate`
- Check `.env` file has API keys
- See [backend/SETUP.md](backend/SETUP.md) troubleshooting section

### iOS won't connect to backend
- Check backend server is running: `cd backend && python main.py`
- Check API URL in `ios/AIPodcast/Utils/Constants.swift`
- For physical device: Use Mac's IP address, not `localhost`

### API key errors
- Never commit `.env` file to git
- Check `.env.example` for required keys
- Get keys from [Your Name]

---

## Contributing

### Code Style

**Python (Backend):**
- Follow PEP 8
- Use `black` for formatting: `black .`
- Add docstrings to functions
- Keep functions small and focused

**Swift (iOS):**
- Follow Swift API Design Guidelines
- Use SwiftLint if configured
- Clear, descriptive variable names
- Comment complex logic

### Pull Request Process

1. Create branch from `main`
2. Make your changes
3. Test thoroughly
4. Create PR with clear description
5. Tag Jesse Hernandez for review
6. Address feedback
7. Merge after approval

---

## Learning Resources

**Backend:**
- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)
- [LangChain Docs](https://python.langchain.com/docs/get_started/introduction)
- [Python Virtual Environments](https://realpython.com/python-virtual-environments-a-primer/)

**iOS:**
- [SwiftUI Tutorials](https://developer.apple.com/tutorials/swiftui)
- [AVFoundation Guide](https://developer.apple.com/documentation/avfoundation)
- [Speech Framework](https://developer.apple.com/documentation/speech)

**Git:**
- [Git Basics](https://git-scm.com/book/en/v2/Getting-Started-Git-Basics)
- [GitHub Flow](https://guides.github.com/introduction/flow/)

---

## Need Help?

1. **Check the docs** - Start with README and SETUP guides
2. **Search Slack** - Someone may have asked already
3. **Ask in Slack** - group chat
4. **Reach out to** - Jesse Hernandez

**When asking for help, include:**
- What you're trying to do
- What you expected to happen
- What actually happened (error messages)
- What you've already tried

---
