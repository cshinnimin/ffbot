from typing import Any, Dict, List, Optional
import requests

from .base import LlmClient

class OpenRouterClient(LlmClient):
    def chat(self, messages: List[Dict[str, Any]], temperature: Optional[float] = None) -> Dict[str, Any]:
        url = "https://openrouter.ai/api/v1/chat/completions"
        model = self.config.get("LLM_MODEL")
        api_key = self.config.get("LLM_API_KEY")

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
            return data['error']['message']

        try:
            return data['choices'][0]['message']['content']
        except Exception:
            return str(data)
