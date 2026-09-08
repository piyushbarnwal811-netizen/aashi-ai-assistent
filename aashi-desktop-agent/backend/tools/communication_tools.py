from __future__ import annotations

import os
import webbrowser
from urllib.parse import quote


def send_email(to: str, subject: str, body: str) -> str:
	url = f"mailto:{quote(to)}?subject={quote(subject)}&body={quote(body)}"
	webbrowser.open(url)
	return f"Email draft opened for {to}"


def send_whatsapp(phone: str, message: str) -> str:
	normalized = "".join(character for character in phone if character.isdigit() or character == "+")
	if not normalized:
		raise ValueError("A phone number is required")
	webbrowser.open(f"https://wa.me/{normalized.lstrip('+')}?text={quote(message)}")
	return "WhatsApp message draft opened"
