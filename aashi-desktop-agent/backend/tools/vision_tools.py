from __future__ import annotations

import os


def capture_screen(output_path: str = "screenshot.png") -> str:
    import pyautogui

    absolute_path = os.path.abspath(output_path)
    screenshot = pyautogui.screenshot()
    screenshot.save(absolute_path)
    return absolute_path