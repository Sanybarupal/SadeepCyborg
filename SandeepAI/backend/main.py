"""Sandeep AI - lightweight Windows desktop assistant starter.
All filesystem access is restricted to the workspace directory.
"""
from pathlib import Path
from urllib.parse import urlparse
import os
import webbrowser

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent
WORKSPACE = (BASE_DIR / "workspace").resolve()
FRONTEND = BASE_DIR / "frontend"
WORKSPACE.mkdir(exist_ok=True)

app = FastAPI(title="Sandeep AI", version="0.1.0")
app.mount("/static", StaticFiles(directory=FRONTEND), name="static")

class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)

class OpenSiteRequest(BaseModel):
    url: str = Field(min_length=8, max_length=2048)

class ReadFileRequest(BaseModel):
    path: str = Field(min_length=1, max_length=500)


def safe_workspace_path(relative: str) -> Path:
    target = (WORKSPACE / relative).resolve()
    if target != WORKSPACE and WORKSPACE not in target.parents:
        raise HTTPException(status_code=403, detail="Workspace के बाहर की file access नहीं कर सकते।")
    return target

@app.get("/")
def home():
    return FileResponse(FRONTEND / "index.html")

@app.get("/api/status")
def status():
    return {"name": "Sandeep AI", "version": "0.1.0", "ai_connected": bool(os.getenv("OPENAI_API_KEY")), "workspace": str(WORKSPACE)}

@app.post("/api/chat")
def chat(payload: ChatRequest):
    """Use online AI only when the user has configured their own API key."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return {"reply": "Sandeep AI का local starter चालू है। Online AI जोड़ने के लिए अपनी API key को backend की .env file में रखें। अभी मैं website खोलने और workspace files देखने जैसे local tools चला सकता हूँ।", "mode": "local"}
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
        response = client.responses.create(
            model=model,
            instructions=(
                "You are Sandeep AI, a careful Windows desktop assistant. "
                "Explain actions before they happen. Never claim to have performed an action unless a tool result confirms it. "
                "Do not ask for passwords, API keys, or private credentials. For destructive or external actions, ask for explicit approval. "
                "You cannot directly control the computer from this chat endpoint; use only the app's listed local tools."
            ),
            input=payload.message,
        )
        return {"reply": response.output_text, "mode": "online"}
    except Exception as exc:
        return {"reply": f"AI connection error: {type(exc).__name__}. API key, network और billing settings जाँचें।", "mode": "error"}

@app.post("/api/open-site")
def open_site(payload: OpenSiteRequest):
    parsed = urlparse(payload.url.strip())
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        raise HTTPException(status_code=400, detail="केवल valid http/https website URL स्वीकार है।")
    webbrowser.open(payload.url.strip(), new=2)
    return {"ok": True, "message": "Website आपके default browser में खोलने का अनुरोध भेज दिया गया।"}

@app.get("/api/files")
def list_files():
    items = []
    for path in WORKSPACE.rglob("*"):
        if path.is_file():
            items.append({"path": path.relative_to(WORKSPACE).as_posix(), "size": path.stat().st_size})
            if len(items) >= 200:
                break
    return {"files": items}

@app.post("/api/read-file")
def read_file(payload: ReadFileRequest):
    path = safe_workspace_path(payload.path)
    if not path.is_file():
        raise HTTPException(status_code=404, detail="File नहीं मिली।")
    if path.stat().st_size > 200_000:
        raise HTTPException(status_code=413, detail="Starter version में 200 KB से बड़ी files पढ़ना disabled है।")
    try:
        content = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        raise HTTPException(status_code=415, detail="यह text file नहीं है या UTF-8 में नहीं है।")
    return {"path": payload.path, "content": content}

@app.get("/api/health")
def health():
    return {"ok": True}
