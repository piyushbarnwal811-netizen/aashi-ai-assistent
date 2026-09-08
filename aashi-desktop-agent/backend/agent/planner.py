from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from backend.database.models import log_action
from backend.security.policy_engine import PolicyEngine
from backend.tools import get_tool


@dataclass
class ToolCall:
	name: str
	arguments: dict[str, Any] = field(default_factory=dict)


@dataclass
class ToolResult:
	name: str
	success: bool
	result: Any = None
	error: str | None = None
	requires_approval: bool = False


class Planner:
	def __init__(self, policy: PolicyEngine | None = None):
		self.policy = policy or PolicyEngine()

	def execute(self, calls: list[ToolCall], approved_actions: set[str] | None = None) -> list[ToolResult]:
		approved_actions = approved_actions or set()
		results: list[ToolResult] = []
		for call in calls:
			decision = self.policy.check(call.name)
			if not decision.allowed:
				result = ToolResult(call.name, False, error=decision.reason, requires_approval=True)
				log_action(call.name, "blocked", decision.reason)
				results.append(result)
				continue
			if decision.requires_approval and call.name not in approved_actions:
				result = ToolResult(call.name, False, error=decision.reason, requires_approval=True)
				log_action(call.name, "approval_required", decision.reason)
				results.append(result)
				continue
			tool = get_tool(call.name)
			if tool is None:
				result = ToolResult(call.name, False, error="Unknown tool")
				log_action(call.name, "failed", "Unknown tool")
				results.append(result)
				continue
			try:
				value = tool(**call.arguments)
				result = ToolResult(call.name, True, result=value)
				log_action(call.name, "success", str(value))
			except Exception as exc:
				result = ToolResult(call.name, False, error=str(exc))
				log_action(call.name, "failed", str(exc))
			results.append(result)
		return results
