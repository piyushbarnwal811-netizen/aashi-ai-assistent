from __future__ import annotations

from pathlib import Path


def transcribe_audio(audio_path: str, language: str = "hi") -> str:
	"""Transcribe an audio file with faster-whisper when it is installed."""
	try:
		from faster_whisper import WhisperModel
	except ImportError as exc:
		raise RuntimeError("faster-whisper is not installed") from exc
	model = WhisperModel("base", compute_type="int8")
	segments, _ = model.transcribe(str(Path(audio_path)), language=language)
	return " ".join(segment.text.strip() for segment in segments).strip()
