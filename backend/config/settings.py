"""
Configuration settings loaded from environment variables.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
BRAVE_SEARCH_API_KEY = os.getenv("BRAVE_SEARCH_API_KEY")

# Validate required keys
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment variables")
if not ELEVENLABS_API_KEY:
    raise ValueError("ELEVENLABS_API_KEY not found in environment variables")

# Server settings
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# Directories
UPLOAD_DIR = BASE_DIR / "uploads"
PODCAST_DIR = BASE_DIR / "generated" / "podcasts"
ANSWER_DIR = BASE_DIR / "generated" / "answers"

# Create directories if they don't exist
UPLOAD_DIR.mkdir(exist_ok=True)
PODCAST_DIR.mkdir(parents=True, exist_ok=True)
ANSWER_DIR.mkdir(parents=True, exist_ok=True)

# Voice settings
VOICE_HOST_A = os.getenv("DEFAULT_VOICE_HOST_A", "21m00Tcm4TlvDq8ikWAM")  # Rachel
VOICE_HOST_B = os.getenv("DEFAULT_VOICE_HOST_B", "pNInz6obpgDQGcFmaJgB")  # Adam

# LLM settings
DEFAULT_MODEL = "gpt-4"
DEFAULT_MAX_TOKENS = 1500
DEFAULT_TEMPERATURE = 0.7

# Document processing
CHUNK_SIZE = 2000
CHUNK_OVERLAP = 200