# Sandeep AI — Windows Starter v0.1

A lightweight local-first desktop assistant starter for Windows 11. It includes a browser UI, optional OpenAI Responses API chat, opening a website in the default browser, and workspace-only file listing/reading.

## Requirements
- Windows 11
- Python 3.11+ (Python 3.12 or 3.13 recommended for broad package compatibility)
- Internet connection for package installation and optional online AI

## Install
Open PowerShell in this folder:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```

Optional browser automation browser install:

```powershell
playwright install chromium
```

## Run

```powershell
uvicorn backend.main:app --reload
```

Open http://127.0.0.1:8000 in your browser.

## Optional online AI
Edit `.env` and add your own API key:

```env
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4.1-mini
```

Restart the server after changing `.env`. API usage may incur separate charges. Do not commit `.env` or share the key.

## Safety boundaries in v0.1
- File browsing and reading are restricted to `workspace/`.
- File reading is limited to 200 KB and UTF-8 text files.
- Website opening accepts only HTTP/HTTPS URLs and uses your default browser.
- This starter does not run arbitrary terminal commands, delete files, submit forms, send messages, or perform purchases.
- Voice input depends on browser Speech Recognition support and browser permissions.

## Current status
The first runnable foundation is included. Playwright browser inspection, VS Code editing, controlled desktop actions, approval queue, persistent chat history, and Windows packaging are planned next; they are not represented as completed features yet.
