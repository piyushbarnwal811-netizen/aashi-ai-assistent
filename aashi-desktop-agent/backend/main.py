from __future__ import annotations

import json
from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, File, HTTPException, UploadFile, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from backend.agent.intent_parser import intent_parser
from backend.agent.memory import ConversationMemory, personal_notes, remember_note
from backend.config import config
from backend.database.db import initialize_database
from backend.voice.stt import transcribe_audio
from backend.voice.tts import speak_text_async

app = FastAPI(title="AASHI Desktop Agent API", version="1.0.0")

# Enable CORS for Tauri Frontend Connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CommandRequest(BaseModel):
    command: str = Field(min_length=1, max_length=10000)
    session_id: str = Field(default="default", min_length=1, max_length=100)
    approved_actions: list[str] = Field(default_factory=list)
    speak: bool = False


class NoteRequest(BaseModel):
    note: str = Field(min_length=1, max_length=5000)


@app.on_event("startup")
def startup() -> None:
    initialize_database()

@app.get("/")
def root():
    return {"status": "online", "agent": "AASHI AI Companion", "voice": config.voice_name}


@app.get("/health")
def health():
    return {"status": "ok", "gemini_configured": bool(config.gemini_api_key)}

@app.post("/api/command")
async def execute_command(req: CommandRequest):
    result = intent_parser.process_command(req.command, req.session_id, set(req.approved_actions))
    audio_file = None
    if req.speak:
        try:
            audio_file = await speak_text_async(result["reply"])
        except RuntimeError as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc

    return {
        "text_response": result["reply"],
        "tool_results": result["tool_results"],
        "audio_path": audio_file,
        "status": "success"
    }


@app.get("/api/history/{session_id}")
def history(session_id: str, limit: int = 20):
    return {"session_id": session_id, "messages": ConversationMemory(session_id).history(limit)}


@app.post("/api/notes")
def add_note(req: NoteRequest):
    remember_note(req.note)
    return {"status": "saved"}


@app.get("/api/notes")
def notes(limit: int = 50):
    return {"notes": personal_notes(limit)}


@app.post("/api/transcribe")
async def transcribe(file: UploadFile = File(...)):
    suffix = Path(file.filename or "audio.wav").suffix or ".wav"
    temporary_path = config.media_dir / f"upload-{uuid4().hex}{suffix}"
    try:
        temporary_path.write_bytes(await file.read())
        text = transcribe_audio(str(temporary_path))
        return {"text": text}
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    finally:
        temporary_path.unlink(missing_ok=True)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            payload = json.loads(await websocket.receive_text())
            request = CommandRequest.model_validate(payload)
            result = intent_parser.process_command(request.command, request.session_id, set(request.approved_actions))
            await websocket.send_json({"type": "response", "text_response": result["reply"], "tool_results": result["tool_results"]})
    except WebSocketDisconnect:
        return
    except Exception as exc:
        await websocket.send_json({"type": "error", "detail": str(exc)})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host=config.host, port=config.port, reload=True)