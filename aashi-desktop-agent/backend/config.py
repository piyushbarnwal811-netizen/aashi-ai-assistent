from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv


BACKEND_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BACKEND_DIR.parent
load_dotenv(PROJECT_DIR / ".env")


class Config:
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    picovoice_key: str = os.getenv("PICOVOICE_PORCUPINE_KEY", "")
    db_path: Path = Path(os.getenv("DB_PATH", str(BACKEND_DIR / "database" / "aashi.db"))).expanduser()
    media_dir: Path = Path(os.getenv("MEDIA_DIR", str(BACKEND_DIR / "data" / "media"))).expanduser()
    security_policy_path: Path = PROJECT_DIR / "config" / "security_policy.json"
    voice_name: str = os.getenv("VOICE_NAME", "hi-IN-SwaraNeural")
    host: str = os.getenv("HOST", "127.0.0.1")
    port: int = int(os.getenv("PORT", "8000"))
    cors_origins: list[str] = [origin.strip() for origin in os.getenv("CORS_ORIGINS", "*").split(",") if origin.strip()]

    @property
    def GEMINI_API_KEY(self) -> str:
        return self.gemini_api_key

    @property
    def PICOVOICE_KEY(self) -> str:
        return self.picovoice_key

    @property
    def DB_PATH(self) -> str:
        return str(self.db_path)

    @property
    def VOICE_NAME(self) -> str:
        return self.voice_name


config = Config()
config.db_path.parent.mkdir(parents=True, exist_ok=True)
config.media_dir.mkdir(parents=True, exist_ok=True)