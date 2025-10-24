from typing import Any, Dict, List, Optional
import requests

from .base import ChatCompletionClientBase

class OllamaChatCompletionClient(ChatCompletionClientBase):
    def chat(self, messages: List[Dict[str, Any]], temperature: Optional[float] = None) -> Dict[str, Any]:
        port = self.config.get("LLM_PORT") or "11434"
        url = "http://localhost:" + port +  "/api/chat"
        model = self.config.get("LLM_MODEL")
        keep_alive = self.config.get("LLM_KEEP_ALIVE", "30m")

        headers = {
            "Content-Type": "application/json"
        }

        payload: Dict[str, Any] = {
            "model": model,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": temperature if temperature is not None else self.config.get("LLM_TEMPERATURE"),
            },
            "keep_alive": keep_alive,
            "temperature": temperature if temperature is not None else self.config.get("LLM_TEMPERATURE")
        }

        data = self._post(url, headers, payload, timeout=60)

        try:
            if isinstance(data, dict) and data.get('error') and data['error'].get('message'):
                return '{"answer": "' + data['error']['message'] + '"}'

            return data['message']['content']
        except Exception:
            return str(data)
