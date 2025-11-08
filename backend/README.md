# AI Interactive Podcast - Backend API

Backend service for generating AI-powered interactive podcasts from documents.

## Quick Start

### Prerequisites
- Python 3.10 or higher
- pip package manager
- API keys for: OpenAI, ElevenLabs, Brave Search

### Setup Instructions

1. **Navigate to backend directory**
```bash
   cd backend
```

2. **Create virtual environment**
```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
   pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
   cp .env.example .env
   # Edit .env and add your API keys
```

5. **Run the server**
```bash
   python main.py
```

6. **Test it's working**
   - Open browser to http://localhost:8000
   - Visit http://localhost:8000/docs for interactive API documentation

## Project Structure
```
backend/
├── main.py              # FastAPI app entry point
├── config/              # Configuration and settings
├── api/routes/          # API endpoint definitions
├── services/            # Business logic
├── database/            # Vector database operations
├── utils/               # Helper functions
├── prompts/             # LLM prompt templates
├── uploads/             # Uploaded documents (gitignored)
└── generated/           # Generated audio files (gitignored)
```

## API Endpoints

See [API_SPEC.md](../docs/API_SPEC.md) for complete API documentation.

**Quick reference:**
- `POST /api/documents/upload` - Upload PDF document
- `POST /api/podcasts/generate` - Generate podcast from documents
- `POST /api/questions/ask` - Ask question about content

## Development

### Running Tests
```bash
pytest tests/
```

### Code Formatting
```bash
black .
```

### Check API Documentation
While server is running, visit: http://localhost:8000/docs

## Troubleshooting

**Import errors:**
- Make sure virtual environment is activated
- Reinstall: `pip install -r requirements.txt`

**API key errors:**
- Check `.env` file has all required keys
- No extra spaces around `=` in `.env`

**Port already in use:**
- Change port: `uvicorn main:app --reload --port 8001`

## Need Help?

- Check [SETUP.md](SETUP.md) for detailed setup guide
- Post in #apprentice-ai-podcast group chat
- Reach out to Jesse Hernandez