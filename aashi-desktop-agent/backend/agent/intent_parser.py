from __future__ import annotations

import re
from typing import Any

from backend.agent.memory import ConversationMemory
from backend.agent.planner import Planner, ToolCall
from backend.agent.prompts import AASHI_SYSTEM_PROMPT
from backend.config import config


class IntentParser:
    def __init__(self, planner: Planner | None = None):
        self.planner = planner or Planner()
        self.model_name = "gemini-1.5-flash"
        self.client = None
        if config.gemini_api_key:
            try:
                from google import genai

                self.client = genai.Client(api_key=config.gemini_api_key)
            except Exception:
                self.client = None

    def _gemini_reply(self, prompt: str, context: str) -> str | None:
        if self.client is None:
            return None
        try:
            from google.genai import types

            response = self.client.models.generate_content(
                model=self.model_name,
                contents=f"Conversation:\n{context}\n\nUser:\n{prompt}",
                config=types.GenerateContentConfig(system_instruction=AASHI_SYSTEM_PROMPT, temperature=0.7),
            )
            return response.text.strip() if response.text else None
        except Exception:
            return None

    def _local_tool_call(self, prompt: str) -> ToolCall | None:
        text = prompt.strip()
        lower = text.lower()
        volume = re.search(r"(?:volume|आवाज).{0,10}(\d{1,3})", lower)
        brightness = re.search(r"(?:brightness|रोशनी).{0,10}(\d{1,3})", lower)
        if volume:
            return ToolCall("os.volume", {"level": int(volume.group(1))})
        if brightness:
            return ToolCall("os.brightness", {"level": int(brightness.group(1))})
        if "screenshot" in lower or "स्क्रीनशॉट" in lower:
            return ToolCall("vision.capture_screen", {})
        if "youtube" in lower:
            query = re.sub(r".*youtube(?: पर| me| on)?\s*", "", text, flags=re.I).strip() or text
            return ToolCall("media.youtube", {"query": query})
        return None

    def process_command(self, user_prompt: str, session_id: str = "default", approved_actions: set[str] | None = None) -> dict[str, Any]:
        memory = ConversationMemory(session_id)
        memory.add("user", user_prompt)
        call = self._local_tool_call(user_prompt)
        if call:
            result = self.planner.execute([call], approved_actions)[0]
            if result.requires_approval:
                reply = f"इस action के लिए आपकी approval चाहिए: {call.name}"
            elif result.success:
                reply = str(result.result)
            else:
                reply = f"Action पूरा नहीं हो पाया: {result.error}"
            memory.add("assistant", reply)
            return {"reply": reply, "tool_results": [result.__dict__]}
        reply = self._gemini_reply(user_prompt, memory.context())
        reply = reply or "मैं समझ गई। Gemini API key उपलब्ध होने पर मैं इस request को और बेहतर तरीके से पूरा कर सकती हूँ।"
        memory.add("assistant", reply)
        return {"reply": reply, "tool_results": []}


intent_parser = IntentParser()