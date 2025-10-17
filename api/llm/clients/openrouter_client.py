from typing import Any, Dict, List, Optional
import requests

from .base import LlmClient


class OpenRouterClient(LlmClient):
    def chat(self, messages: List[Dict[str, Any]], stream: bool = False, temperature: Optional[float] = None) -> Dict[str, Any]:
        url = self.config.get("LLM_URL") or "https://openrouter.ai/api/v1/chat/completions"
        model = self.config.get("LLM_MODEL")
        api_key = self.config.get("LLM_API_KEY")

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        }

        payload: Dict[str, Any] = {
            "model": model,
            "messages": messages,
            "temperature": temperature if temperature is not None else self.config.get("LLM_TEMPERATURE"),
            # For OpenRouter and Ollama we can include options/keep_alive analogs if supported
        }

        print(f"[OpenRouterClient] POST {url} model={model} msgs={len(messages)}")
        res = requests.post(url, headers=headers, json=payload, timeout=60)
        # Return shape similar to OpenAI (choices)
        res.raise_for_status()
        return res.json()


