# Backend Setup Guide

Follow these steps to get your development environment running.

---

## Prerequisites Check

Before starting, verify you have the required software installed.

### Check Python Version

Open Terminal and run:
```bash
python3 --version
```

**What you should see:** Python 3.10.0 or higher

**If you don't have Python or have an older version:**
- **Mac:** 
  - Option 1: Download from [python.org](https://www.python.org/downloads/)
  - Option 2: Use Homebrew: `brew install python@3.10`
- **Windows:** Download from [python.org](https://www.python.org/downloads/)

### Check pip is Available
```bash
pip3 --version
```

**What you should see:** pip version number (e.g., pip 23.x.x)

pip comes automatically with Python, so if Python installed correctly, pip should work.

---

## Installation Steps

### Step 1: Open Terminal and Navigate to Backend
```bash
# From the project root directory
cd backend
```

**Verify you're in the right place:**
```bash
pwd
```
Should show something like: `.../ai-interactive-podcast/backend`

---

### Step 2: Create a Virtual Environment

A virtual environment is like a separate sandbox for this project's Python packages. This keeps your project dependencies isolated from other Python projects.
```bash
python3 -m venv venv
```

**What this does:** Creates a folder called `venv/` inside your `backend/` directory

**Wait time:** 10-30 seconds

**What you'll see:** A new `venv/` folder appears (you won't see much output in terminal)

---

### Step 3: Activate the Virtual Environment

This tells your terminal to use the Python from your virtual environment instead of your system Python.

**On Mac/Linux:**
```bash
source venv/bin/activate
```

**On Windows:**
```bash
venv\Scripts\activate
```

**How to know it worked:**

You should see `(venv)` appear at the start of your terminal prompt:
```bash
(venv) your-computer:backend your-name$
```

**Important:** You need to activate the virtual environment **every time** you open a new terminal window to work on this project.

---

### Step 4: Install Python Packages

Now install all the packages this project needs:
```bash
pip install -r requirements.txt
```

**What this does:** Installs FastAPI, OpenAI library, LangChain, and other dependencies

**Wait time:** 1-3 minutes

**What you'll see:** Lots of text scrolling as packages download and install

**When it's done:** You'll see "Successfully installed..." with a list of packages

---

### Step 5: Set Up Environment Variables

Environment variables store sensitive information like API keys.

**Copy the example file:**
```bash
cp .env.example .env
```

**Now edit the `.env` file:**

Open `.env` in VSCode or any text editor. You'll see:
```bash
OPENAI_API_KEY=sk-your-key-here
ELEVENLABS_API_KEY=your-key-here
BRAVE_SEARCH_API_KEY=your-key-here
```

**Replace the placeholder values with actual API keys:**

Get the API keys from Jesse Hernandez, then update the file to look like:
```bash
OPENAI_API_KEY=sk-proj-abc123...
ELEVENLABS_API_KEY=sk_abc123...
BRAVE_SEARCH_API_KEY=BSA...
```

**Important rules for .env files:**
- ❌ No spaces around the `=` sign
- ❌ Don't use quotes around values
- ❌ Never commit this file to git (it's already in .gitignore)
- ✅ Keep your API keys secret

**Save the file.**

---

### Step 6: Verify Installation

Let's make sure everything installed correctly:
```bash
# Test FastAPI
python3 -c "import fastapi; print('✅ FastAPI installed successfully!')"

# Test OpenAI
python3 -c "import openai; print('✅ OpenAI installed successfully!')"

# Test LangChain
python3 -c "import langchain; print('✅ LangChain installed successfully!')"
```

**What you should see:** Three success messages with checkmarks

**If you see errors:** Make sure your virtual environment is activated (see `(venv)` in prompt?)

---

### Step 7: Test API Keys

Quick test to make sure your API keys work:
```bash
python3 -c "from config.settings import OPENAI_API_KEY; print('✅ API keys loaded!' if OPENAI_API_KEY else '❌ Keys not found')"
```

**What you should see:** `✅ API keys loaded!`

**If you see an error:**
- Check `.env` file is in the `backend/` directory
- Check `.env` has your actual API keys (not the placeholder text)
- Check no typos in the variable names

---

### Step 8: Run the Server

Time to start the backend server!
```bash
python main.py
```

**Alternative command (does the same thing):**
```bash
uvicorn main:app --reload
```

**What you should see:**
```
INFO:     Will watch for changes in these directories: ['/path/to/backend']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**The server is now running!** Don't close this terminal window.

---

### Step 9: Test the Server in Your Browser

Keep the server running and open a new browser tab.

**Test 1: Health Check**

Go to: http://localhost:8000

**What you should see:**
```json
{
  "message": "AI Interactive Podcast API",
  "status": "healthy",
  "version": "1.0.0"
}
```

**Test 2: API Documentation**

Go to: http://localhost:8000/docs

**What you should see:** 
- An interactive API documentation page (Swagger UI)
- This is automatically generated by FastAPI!
- You can test API endpoints directly from this page

**If both tests work:** 🎉 **Success! Your backend is running!**

---

## Daily Workflow

Every time you start working on the backend, follow these steps:
```bash
# 1. Navigate to backend directory
cd backend

# 2. Activate virtual environment
source venv/bin/activate  # Mac/Linux
# or
venv\Scripts\activate  # Windows

# 3. Start the server
python main.py

# Keep this terminal open while you work
```

When you're done working:
```bash
# Press CTRL+C to stop the server

# Deactivate virtual environment (optional)
deactivate
```

---

## Troubleshooting

### Problem: "python3: command not found"

**Solution:** Python is not installed. Install from [python.org](https://www.python.org/downloads/)

---

### Problem: "No module named 'fastapi'"

**Cause:** Virtual environment is not activated, or packages not installed

**Solution:**
```bash
# Make sure you see (venv) in your prompt
source venv/bin/activate

# Reinstall packages
pip install -r requirements.txt
```

---

### Problem: "OPENAI_API_KEY not found in environment"

**Cause:** `.env` file is missing or incorrect

**Solution:**
1. Make sure `.env` file exists in `backend/` directory (not `backend/venv/` or elsewhere)
2. Open `.env` and check:
   - File is named exactly `.env` (not `.env.txt`)
   - API keys are filled in (not placeholder text)
   - No spaces around `=` signs
   - No quotes around values

Example of correct `.env`:
```bash
OPENAI_API_KEY=sk-proj-abc123def456
ELEVENLABS_API_KEY=sk_987654321
```

---

### Problem: "Address already in use" or "Port 8000 already in use"

**Cause:** Another program is using port 8000

**Solution Option 1:** Use a different port
```bash
uvicorn main:app --reload --port 8001
```

Then access at http://localhost:8001

**Solution Option 2:** Stop the other program using port 8000
```bash
# Find what's using port 8000
lsof -i :8000

# Kill that process (use the PID from above command)
kill <PID>
```

---

### Problem: Virtual environment won't activate

**Solution:** Delete and recreate it
```bash
# Remove old venv
rm -rf venv

# Create new one
python3 -m venv venv

# Activate it
source venv/bin/activate

# Reinstall packages
pip install -r requirements.txt
```

---

### Problem: "ImportError: cannot import name..."

**Cause:** Some packages didn't install correctly

**Solution:**
```bash
# Reinstall specific package
pip install --force-reinstall <package-name>

# Or reinstall everything
pip install --force-reinstall -r requirements.txt
```

---

### Problem: Server starts but browser shows "Connection refused"

**Cause:** Server not actually running, or wrong URL

**Solution:**
1. Check terminal - do you see "Uvicorn running on..."?
2. Look for error messages in terminal
3. Try http://127.0.0.1:8000 instead of http://localhost:8000
4. Make sure you're not using https:// (use http://)

---

## Understanding the Files

### What is `venv/`?
A folder containing an isolated Python environment for this project. Never edit files in here manually. Don't commit to git (already in .gitignore).

### What is `requirements.txt`?
A list of all Python packages this project needs. Like a shopping list for pip.

### What is `.env`?
Contains secret API keys and configuration. Never commit to git.

### What is `main.py`?
The entry point - starts the FastAPI server.

### What is `config/settings.py`?
Loads configuration from `.env` file and makes it available to other parts of the code.

---

## Next Steps

Once your server is running successfully:

1. ✅ **Check your assigned tickets** in Linear/Jira
2. ✅ **Start with "Setup" tickets** - these help you understand the codebase
3. ✅ **Read through the code files** - understand the structure before making changes
4. ✅ **Test the `/docs` endpoint** - play with the interactive API documentation
5. ✅ **Ask questions** in #apprentice-ai-podcast Slack channel

---

## Useful Commands Reference
```bash
# Activate virtual environment (do this every session)
source venv/bin/activate

# Start server (auto-reloads when you change code)
python main.py

# Run server on different port
uvicorn main:app --reload --port 8001

# Run tests (once we write some)
pytest tests/

# Format code to match Python style guidelines
black .

# Check what packages are installed
pip list

# Deactivate virtual environment when done
deactivate
```

---

## Getting Help

### Stuck for more than 20-30 minutes?

Don't spin your wheels! Ask for help:

**1. Post in Slack (#apprentice-ai-podcast):**

Good question format:
```
I'm trying to: [what you want to accomplish]
I ran: [command you ran]
I expected: [what should happen]
I got: [error message or unexpected behavior]
I've tried: [what you've attempted]
```

**2. Schedule office hours with [Your Name]**

**3. Check these resources:**
- FastAPI docs: https://fastapi.tiangolo.com/
- Python virtual environments: https://realpython.com/python-virtual-environments-a-primer/
- Stack Overflow (for specific error messages)

---

## Tips for Success

✅ **Activate venv every session** - Look for `(venv)` in your prompt

✅ **Read error messages carefully** - They usually tell you exactly what's wrong

✅ **Test small changes frequently** - Don't write 100 lines before testing

✅ **Commit working code often** - Small commits are better than big ones

✅ **Use the /docs endpoint** - It's the easiest way to test your API

✅ **Ask questions early** - Don't waste hours on something someone can explain in 5 minutes

---
