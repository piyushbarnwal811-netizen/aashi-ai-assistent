from __future__ import annotations

from backend.database.db import database, initialize_database


def save_message(session_id: str, role: str, content: str) -> None:
	initialize_database()
	with database() as connection:
		connection.execute(
			"INSERT INTO messages(session_id, role, content) VALUES (?, ?, ?)",
			(session_id, role, content),
		)


def get_messages(session_id: str, limit: int = 20) -> list[dict[str, str]]:
	initialize_database()
	with database() as connection:
		rows = connection.execute(
			"SELECT role, content, created_at FROM messages WHERE session_id = ? ORDER BY id DESC LIMIT ?",
			(session_id, max(1, min(limit, 100))),
		).fetchall()
	return [dict(row) for row in reversed(rows)]


def save_note(note: str) -> None:
	initialize_database()
	with database() as connection:
		connection.execute("INSERT INTO notes(note) VALUES (?)", (note,))


def get_notes(limit: int = 50) -> list[dict[str, str]]:
	initialize_database()
	with database() as connection:
		rows = connection.execute(
			"SELECT note, created_at FROM notes ORDER BY id DESC LIMIT ?",
			(max(1, min(limit, 200)),),
		).fetchall()
	return [dict(row) for row in rows]


def log_action(action: str, status: str, details: str = "") -> None:
	initialize_database()
	with database() as connection:
		connection.execute(
			"INSERT INTO action_logs(action, status, details) VALUES (?, ?, ?)",
			(action, status, details),
		)
