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

        data = self._post(url, headers, payload, timeout=60)

        if isinstance(data, dict) and data.get('error') and data['error'].get('message'):
            return '{answer: "' + data['error']['message'] + '"}'

        # Normal choice shape: choices[0].message.content
        try:
            return data['choices'][0]['message']['content']
        except Exception:
            # Fallback: return the raw JSON as string
            return str(data)


