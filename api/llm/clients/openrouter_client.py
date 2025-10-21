from typing import Any, Dict, List, Optional
import requests

from .base import LlmClient


class OpenRouterClient(LlmClient):
    def chat(self, messages: List[Dict[str, Any]], temperature: Optional[float] = None) -> Dict[str, Any]:
        url = self.config.get("LLM_URL") or "https://openrouter.ai/api/v1/chat/completions"
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

        print(f"[OpenRouterClient] POST {url} model={model} msgs={len(messages)}")
        res = requests.post(url, headers=headers, json=payload, timeout=60)
        # Return shape similar to OpenAI (choices)
        res.raise_for_status()
        data = res.json()
        # openrouter uses OpenAI-like shapes; return error message or first choice
        if isinstance(data, dict) and data.get('error') and data['error'].get('message'):
            return data['error']['message']

        try:
            return data['choices'][0]['message']['content']
        except Exception:
            return str(data)


