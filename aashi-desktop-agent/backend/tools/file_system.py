from __future__ import annotations

import shutil
from pathlib import Path


def _path(value: str) -> Path:
	return Path(value).expanduser().resolve()


def create_folder(path: str) -> str:
	target = _path(path)
	target.mkdir(parents=True, exist_ok=True)
	return f"Folder created: {target}"


def write_file(path: str, content: str) -> str:
	target = _path(path)
	target.parent.mkdir(parents=True, exist_ok=True)
	target.write_text(content, encoding="utf-8")
	return f"File written: {target}"


def read_file(path: str) -> str:
	return _path(path).read_text(encoding="utf-8")


def move_path(source: str, destination: str) -> str:
	target = shutil.move(str(_path(source)), str(_path(destination)))
	return f"Moved to: {target}"


def delete_path(path: str) -> str:
	target = _path(path)
	if target.is_dir():
		shutil.rmtree(target)
	elif target.exists():
		target.unlink()
	return f"Deleted: {target}"
