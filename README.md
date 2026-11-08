# Sandeep AI

Personal Windows 11 AI assistant starter project.

## Project location
The starter application is in [SandeepAI/](./SandeepAI/).

## Quick start
1. Install Python 3.11 or newer.
2. Open PowerShell in the `SandeepAI` folder.
3. Create and activate a virtual environment:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

4. Optionally add your OpenAI API key to the local `.env` file. Never commit that file.
5. Start the app:

```powershell
uvicorn backend.main:app --reload
```

6. Visit http://127.0.0.1:8000.

See [SandeepAI/README.md](./SandeepAI/README.md) for details and safety limitations.

## Current scope
The starter includes a FastAPI backend, chat UI, optional OpenAI Responses API connection, browser URL opening, browser voice-input support, and workspace-restricted text-file listing/reading. It does not yet include full mouse/keyboard control, a coding agent, or autonomous computer operation.
