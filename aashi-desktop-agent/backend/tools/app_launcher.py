from __future__ import annotations

import platform
import subprocess
import webbrowser


def open_url(url: str) -> str:
	webbrowser.open(url)
	return f"Opened {url}"


def launch_application(command: str, *args: str) -> str:
	subprocess.Popen([command, *args], start_new_session=True)
	return f"Launched {command}"


def open_terminal() -> str:
	command = "cmd.exe" if platform.system() == "Windows" else "x-terminal-emulator"
	return launch_application(command)
