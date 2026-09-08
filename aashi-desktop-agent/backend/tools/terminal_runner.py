from __future__ import annotations

import subprocess


def run_command(command: str, cwd: str | None = None, timeout: int = 30) -> dict[str, object]:
	completed = subprocess.run(
		command,
		cwd=cwd,
		shell=True,
		capture_output=True,
		text=True,
		timeout=max(1, min(timeout, 120)),
		check=False,
	)
	return {
		"return_code": completed.returncode,
		"stdout": completed.stdout[-10000:],
		"stderr": completed.stderr[-10000:],
	}
