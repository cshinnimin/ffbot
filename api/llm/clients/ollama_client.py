from typing import Any, Dict, List, Optional
import requests

from .base import LlmClient


class OllamaClient(LlmClient):
    def chat(self, messages: List[Dict[str, Any]], temperature: Optional[float] = None) -> Dict[str, Any]:
        url = self.config.get("LLM_URL") or "http://localhost:11434/api/chat"
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

        print(f"[OllamaClient] POST {url} model={model} msgs={len(messages)}")
        res = requests.post(url, headers=headers, json=payload, timeout=60)
        res.raise_for_status()
        data = res.json()

        try:
            if isinstance(data, dict) and data.get('error') and data['error'].get('message'):
                return '{"answer": "' + data['error']['message'] + '"}'

            return data['message']['content']
        except Exception:
            return str(data)


