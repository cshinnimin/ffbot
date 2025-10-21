import os
from typing import Any, Dict, List, Optional
import requests

from .base import LlmClient


class OpenAIClient(LlmClient):
    def chat(self, messages: List[Dict[str, Any]], temperature: Optional[float] = None) -> Dict[str, Any]:
        url = self.config.get("LLM_URL") or "https://api.openai.com/v1/chat/completions"
        model = self.config.get("LLM_MODEL")
        api_key = self.config.get("LLM_API_KEY") or os.environ.get("LLM_API_KEY")

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        payload: Dict[str, Any] = {
            "model": model,
            "messages": messages,
            "stream": False,
            "temperature": temperature if temperature is not None else self.config.get("LLM_TEMPERATURE")
        }

        # OpenAI expects streaming as SSE; here we do non-streaming to keep parity with frontend
        print(f"[OpenAIClient] POST {url} model={model} msgs={len(messages)}")
        res = requests.post(url, headers=headers, json=payload, timeout=60)
        res.raise_for_status()
        data = res.json()
        # Leave OpenAI response as-is: parseResponse handles choices and error shapes
        return data


