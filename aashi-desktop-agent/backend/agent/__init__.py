"""AASHI's agent orchestration package.

The modules are loaded lazily so importing ``backend.agent`` does not require
optional AI or desktop-integration dependencies immediately.
"""

from __future__ import annotations

from importlib import import_module
from typing import Any


__version__ = "1.0.0"
__all__ = [
	"IntentParser",
	"intent_parser",
	"Planner",
	"ToolCall",
	"ToolResult",
	"ConversationMemory",
]


_EXPORTS = {
	"IntentParser": ("backend.agent.intent_parser", "IntentParser"),
	"intent_parser": ("backend.agent.intent_parser", "intent_parser"),
	"Planner": ("backend.agent.planner", "Planner"),
	"ToolCall": ("backend.agent.planner", "ToolCall"),
	"ToolResult": ("backend.agent.planner", "ToolResult"),
	"ConversationMemory": ("backend.agent.memory", "ConversationMemory"),
}


def __getattr__(name: str) -> Any:
	export = _EXPORTS.get(name)
	if export is None:
		raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
	module = import_module(export[0])
	value = getattr(module, export[1])
	globals()[name] = value
	return value
