# AI Interactive Podcast

An AI-powered interactive learning platform that generates podcast-style discussions from documents and enables real-time Q&A during playback.

**Demo Date:** December 1, 2025  

---

## What This Project Does

Transform passive learning into an interactive conversation:

1. **Upload documents** (PDFs) about any topic you want to learn
2. **AI generates a podcast** with two hosts discussing the content naturally
3. **Listen and interrupt** to ask questions in real-time
4. **Get instant answers** from your documents or web search

Think of it as having a conversation with an AI tutor who has read all your study materials.

---

## Project Vision

Demonstrate how Apple could integrate conversational AI learning into the Podcasts app ecosystem, leveraging unique advantages:
- **Ecosystem integration** - Works with Files, Notes, Safari, Books
- **Privacy-first** - On-device processing with Apple Intelligence
- **Native experience** - AirPods spatial audio, seamless iCloud sync
- **Siri integration** - "Hey Siri, teach me about [topic]"

---

## Project Structure

This is a monorepo containing both backend API and iOS app:
```
ai-interactive-podcast/
├── README.md                    # You are here
├── .gitignore                   # What not to commit
├── docs/                        # Shared documentation
│   ├── ARCHITECTURE.md          # Technical architecture and decisions
│   ├── API_SPEC.md              # Complete API documentation
│   └── DEMO_SCRIPT.md           # Demo day script and preparation
├── backend/                     # Python/FastAPI backend
│   ├── README.md                # Backend overview
│   ├── SETUP.md                 # Step-by-step setup guide
│   ├── main.py                  # FastAPI app entry point
│   ├── requirements.txt         # Python dependencies
│   ├── .env.example             # Environment variables template
│   ├── config/                  # Configuration management
│   ├── api/routes/              # API endpoint definitions
│   ├── services/                # Business logic (document processing, podcast generation, Q&A)
│   ├── database/                # Vector database operations (Chroma)
│   ├── prompts/                 # LLM prompt templates
│   ├── utils/                   # Helper functions
│   ├── uploads/                 # Uploaded documents (gitignored)
│   └── generated/               # Generated audio files (gitignored)
└── frontend/                    # Frontend applications
    └── ios/                     # Swift/SwiftUI iOS app
        ├── README.md            # iOS overview
        ├── SETUP.md             # Step-by-step setup guide
        ├── AIPodcast.xcodeproj/ # Xcode project file
        └── AIPodcast/           # iOS source code
            ├── Views/           # SwiftUI views
            ├── ViewModels/      # State management
            ├── Models/          # Data structures
            ├── Services/        # API client, audio player, speech
            └── Utils/           # Constants and helpers
```

---

## Team

| Role | Responsibilities |
|------|------------------|
| **Technical Lead** | Architecture, code reviews, integration, technical decisions |
| **Backend Engineer** | Python/FastAPI, document processing, podcast generation, Q&A |
| **iOS Engineer** | SwiftUI, audio playback, UI/UX, speech recognition |
| **Product Manager #1** | Market research, competitive analysis, business case |
| **Product Manager #2** | Presentation deck, demo script, logistics |

---

## Getting Started

### Prerequisites

**For Backend:**
- Python 3.10+
- pip package manager
- API keys (OpenAI, ElevenLabs, Brave Search)

**For iOS:**
- macOS 14.0+
- Xcode 15.0+
- iOS 17.0+ device or simulator

**For Everyone:**
- Git (for version control)
- Slack (for team communication)

---

### Clone the Repository
```bash
# Clone the repo
git clone https://github.com/jdez23/ai-interactive-podcast.git

# Navigate into the project
cd ai-interactive-podcast
```

---

### Backend Setup
```bash
# Navigate to backend
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # Mac/Linux
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your API keys

# Run the server
python main.py

# Server will run at http://localhost:8000
# API docs available at http://localhost:8000/docs
```

**Full instructions:** See [backend/SETUP.md](backend/SETUP.md)

---

### iOS Setup
```bash
# Navigate to iOS directory
cd frontend/ios

# Open project in Xcode
open AIPodcast.xcodeproj
# or
xed .

# In Xcode:
# 1. Update API base URL in Utils/Constants.swift
#    - Simulator: http://localhost:8000
#    - Physical device: http://YOUR_MAC_IP:8000
# 2. Select target device/simulator
# 3. Press ⌘+R to build and run
```

**Full instructions:** See [frontend/ios/SETUP.md](frontend/ios/SETUP.md)

**Note:** Make sure backend server is running before launching iOS app!

---

## Tech Stack

### Backend
- **FastAPI** - Modern Python web framework with auto-generated docs
- **LangChain** - RAG (Retrieval Augmented Generation) framework
- **Chroma** - Vector database for semantic search
- **OpenAI GPT-4** - Podcast script and Q&A generation
- **ElevenLabs** - Natural voice synthesis
- **Brave Search API** - Web search fallback

### iOS
- **SwiftUI** - Declarative UI framework
- **AVFoundation** - Audio playback
- **Speech Framework** - Voice input
- **Combine** - Reactive state management
- **URLSession** - API networking

---

## Documentation

### Technical Documentation
- **[Technical Architecture](docs/ARCHITECTURE.md)** - System design, technology decisions, data flows
- **[API Specification](docs/API_SPEC.md)** - Complete API endpoint documentation
- **[Demo Script](docs/DEMO_SCRIPT.md)** - Demo day preparation and script

### Setup Guides
- **[Backend Setup](backend/SETUP.md)** - Detailed backend setup instructions
- **[iOS Setup](frontend/ios/SETUP.md)** - Detailed iOS setup instructions

### Project Management
- **Project Hub (Google Doc)** - [Link] - Sprint timeline, tickets, meeting notes
- **PM Deliverables (Google Doc)** - [Link] - PM-specific tasks and metrics

---

## Development Workflow

### Branching Strategy
```bash
# Create a branch for your work
git checkout -b your-name/feature-name

# Examples:
# git checkout -b jesse/document-upload
# git checkout -b sarah/podcast-player-ui

# Make changes, commit regularly
git add .
git commit -m "Descriptive message about what changed"

# Push your branch
git push origin your-name/feature-name

# Create Pull Request on GitHub for review
# Tag [Tech Lead Name] for code review
```

### Commit Guidelines

**Good commit messages:**
- ✅ "Add PDF text extraction to document processor"
- ✅ "Fix audio playback bug when interrupting podcast"
- ✅ "Update API client to handle network errors"

**Bad commit messages:**
- ❌ "Update"
- ❌ "Fixed stuff"
- ❌ "WIP"

**Commit frequency:**
- Commit when you complete a logical unit of work
- Push to GitHub at least daily
- Don't wait until everything is perfect

---

## API Quick Reference

**Base URL:** `http://localhost:8000` (development)

**Key Endpoints:**
- `POST /api/documents/upload` - Upload PDF document
- `GET /api/documents/list` - List uploaded documents
- `POST /api/podcasts/generate` - Generate podcast from documents
- `GET /api/podcasts/{podcast_id}` - Get podcast metadata
- `POST /api/questions/ask` - Ask question during playback

**Interactive API Docs:** http://localhost:8000/docs (when backend is running)

**Full specification:** See [docs/API_SPEC.md](docs/API_SPEC.md)

---

## Troubleshooting

### Backend Issues

**"OPENAI_API_KEY not found in environment"**
- Check `.env` file exists in `backend/` directory
- Verify no spaces around `=` in `.env` file
- Make sure virtual environment is activated

**"Port 8000 already in use"**
- Another process is using port 8000
- Kill the process or use different port: `uvicorn main:app --reload --port 8001`

**"ModuleNotFoundError: No module named 'fastapi'"**
- Virtual environment not activated
- Run: `source venv/bin/activate` (Mac) or `venv\Scripts\activate` (Windows)
- Reinstall: `pip install -r requirements.txt`

---

### iOS Issues

**"Failed to connect to API"**
- Backend server not running? Start with: `cd backend && python main.py`
- Check `Constants.swift` has correct API URL
- For physical device: Use Mac's IP address (find with `ifconfig | grep inet`)
- Ensure Mac and iPhone on same WiFi network

**"No signing certificate found"**
- Xcode → Settings → Accounts → Add your Apple ID
- In project settings → Signing & Capabilities → Select your team

**"Microphone permission denied"**
- Device: Settings → Privacy & Security → Microphone → AIPodcast → ON
- Simulator: Simulator menu → I/O → Input → Internal Microphone

---

### General Issues

**Git conflicts**
- Pull latest changes before starting work: `git pull origin main`
- If conflict occurs, ask [Tech Lead] for help resolving

**Can't find documentation**
- Check this README's links section
- Check docs/ folder
- Ask in Slack

---

## Scope & Priorities

### P0 - Must Have (Required for Demo)
- [ ] Upload 1 PDF document
- [ ] Generate 1 podcast
- [ ] Play podcast audio
- [ ] Interrupt and ask 1 question
- [ ] Get audio answer
- [ ] Basic error handling

### P1 - Should Have (If Time Allows)
- [ ] Multiple documents
- [ ] Natural-sounding voices
- [ ] Web search fallback
- [ ] Waveform visualization

### P2 - Nice to Have (Cut If Behind)
- [ ] Voice input
- [ ] Advanced UI animations
- [ ] Perfect error messages

### Out of Scope (Not Doing)
- User accounts/authentication
- Production deployment
- Multiple file formats
- Comprehensive testing
- Accessibility features

---

## Learning Resources

### Backend
- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/) - Start here!
- [LangChain Documentation](https://python.langchain.com/docs/)
- [Chroma Quickstart](https://docs.trychroma.com/getting-started)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [Python Virtual Environments](https://realpython.com/python-virtual-environments-a-primer/)

### iOS
- [SwiftUI Tutorials](https://developer.apple.com/tutorials/swiftui) - Official Apple tutorials
- [AVFoundation Guide](https://developer.apple.com/documentation/avfoundation)
- [Speech Framework](https://developer.apple.com/documentation/speech)
- [Async/Await in Swift](https://docs.swift.org/swift-book/LanguageGuide/Concurrency.html)
- [Hacking with Swift](https://www.hackingwithswift.com/) - Excellent SwiftUI resources

### General
- [Git Basics](https://git-scm.com/book/en/v2/Getting-Started-Git-Basics)
- [GitHub Flow](https://guides.github.com/introduction/flow/)
- [MVVM Architecture](https://www.hackingwithswift.com/books/ios-swiftui/introducing-mvvm-into-your-swiftui-project)
- [What is RAG?](https://www.promptingguide.ai/techniques/rag)

---

## Success Criteria

### A+ Success (Best Case)
- ✅ Demo works flawlessly
- ✅ Leadership loves it and asks about implementation
- ✅ All team members get full-time offers
- ✅ Feature considered for actual Podcasts app

### A Success (Great Outcome)
- ✅ Demo works with minor hiccups
- ✅ Leadership sees potential
- ✅ Team demonstrates strong collaboration
- ✅ Solidifies full-time conversions

### B Success (Acceptable)
- ✅ Demo has technical issues but concept is clear
- ✅ Leadership understands vision
- ✅ Team built something we're proud of
- ✅ Strong learning experience

**Important:** We're apprentices building something ambitious in 24 days. The goal is to impress with our approach, collaboration, and potential - not to ship production-ready code.

---

## Contributing

### Pull Request Process

1. Create feature branch from `main`
2. Make your changes
3. Test thoroughly locally
4. Commit with clear messages
5. Push to GitHub
6. Create Pull Request with description
7. Tag [Tech Lead] for review
8. Address feedback
9. Merge after approval

### Code Review Guidelines

**As Author:**
- Test your code before requesting review
- Provide context in PR description
- Respond to feedback constructively

**As Reviewer:**
- Be kind and constructive
- Ask questions if something is unclear
- Approve when code meets standards

---

## Demo Day Preparation

### Pre-Demo Checklist (Week 3)
- [ ] Backend features complete and stable
- [ ] iOS features complete and polished
- [ ] Demo content selected and tested
- [ ] Presentation deck finalized
- [ ] 3 full dress rehearsals completed
- [ ] Backup plans documented
- [ ] All devices charged

### Backup Plans
- Pre-generated podcasts (if live generation slow)
- Screen recordings (if features fail)
- Backup device (if primary device crashes)
- iPhone hotspot (if WiFi fails)

**Full preparation details:** See [docs/DEMO_SCRIPT.md](docs/DEMO_SCRIPT.md)

---

## Acknowledgments

Built by Apple apprentices as a demonstration of AI-powered learning experiences integrated into the Apple ecosystem.

**Inspired by:**
- Google's NotebookLM (but with interactivity)
- Apple's design philosophy (simple, integrated, privacy-first)
- The desire to make learning feel like a conversation

---

## Need Help?

1. **Check documentation** - README, SETUP guides, ARCHITECTURE docs
3. **Ask in Slack** - Group chat

**When asking for help, include:**
- What you're trying to do
- What you expected to happen
- What actually happened (error messages, screenshots)
- What you've already tried

---

**Let's build something amazing! 🚀**

*Last updated: November 8, 2025 by [Your Name]*