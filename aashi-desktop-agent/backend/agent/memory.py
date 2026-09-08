from __future__ import annotations

from backend.database.models import get_messages, get_notes, save_message, save_note


class ConversationMemory:
	def __init__(self, session_id: str):
		self.session_id = session_id

	def add(self, role: str, content: str) -> None:
		save_message(self.session_id, role, content)

	def history(self, limit: int = 20) -> list[dict[str, str]]:
		return get_messages(self.session_id, limit)

	def context(self, limit: int = 12) -> str:
		return "\n".join(f"{item['role']}: {item['content']}" for item in self.history(limit))


def remember_note(note: str) -> None:
	save_note(note.strip())


def personal_notes(limit: int = 50) -> list[dict[str, str]]:
	return get_notes(limit)
