from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from backend.config import config


@dataclass(frozen=True)
class PolicyDecision:
	allowed: bool
	requires_approval: bool
	reason: str


class PolicyEngine:
	def __init__(self, policy_path: Path | None = None):
		self.path = policy_path or config.security_policy_path
		self.policy = self._load()

	def _load(self) -> dict:
		if not self.path.exists() or not self.path.read_text(encoding="utf-8").strip():
			return {"safe": [], "sensitive": [], "critical": []}
		try:
			return json.loads(self.path.read_text(encoding="utf-8"))
		except json.JSONDecodeError:
			return {"safe": [], "sensitive": [], "critical": []}

	def check(self, action: str) -> PolicyDecision:
		normalized = action.lower()
		for category, values in self.policy.items():
			if any(normalized == value.lower() or normalized.startswith(f"{value.lower()}.") for value in values):
				if category == "critical":
					return PolicyDecision(False, True, "Critical actions are disabled by policy")
				if category == "sensitive":
					return PolicyDecision(True, True, "User approval is required")
				return PolicyDecision(True, False, "Allowed by policy")
		return PolicyDecision(True, False, "No restriction matched")
