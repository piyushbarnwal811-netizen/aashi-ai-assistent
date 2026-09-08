from __future__ import annotations

import asyncio
from pathlib import Path

from backend.config import config


async def speak_text_async(text: str, output_path: str = "temp_response.mp3"):
    try:
        import edge_tts
    except ImportError as exc:
        raise RuntimeError("edge-tts is not installed") from exc

    target = Path(output_path)
    if not target.is_absolute():
        target = config.media_dir / target
    communicate = edge_tts.Communicate(text, config.voice_name)
    await communicate.save(str(target))
    return str(target)

def speak(text: str):
    return asyncio.run(speak_text_async(text))