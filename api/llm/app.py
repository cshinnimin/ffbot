from flask import Flask, request, jsonify
from flask_cors import CORS
from time import sleep
import os
import requests
from .config import get_config
from .chat_completion_client import create_client

def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app)

    config = get_config()

    # Instantiate client via registry-based factory
    provider = config["LLM_PROVIDER"].lower()
    client = create_client(config)
    print(f"[LLM API] Initialized provider '{provider}' with model '{config.get('LLM_MODEL')}'")

    @app.route("/llm/config", methods=["GET", "OPTIONS"])
    def get_public_config():
        if request.method == "OPTIONS":
            return ("", 200)
        # Return only non-sensitive config for the React app
        public_config = {
            "provider": provider,
            "model": config.get("LLM_MODEL"),
            "temperature": float(config.get("LLM_TEMPERATURE", 0.4)),
            "keep_alive": config.get("LLM_KEEP_ALIVE", ""),
            "throttle_delay": int(config.get("LLM_THROTTLE_DELAY", 0)),
        }
        return jsonify(public_config)

    @app.route("/llm/get_response", methods=["POST", "OPTIONS"])
    def get_response():
        if request.method == "OPTIONS":
            return ("", 200)
        payload = request.get_json(silent=True) or {}
        conversation = payload.get("messages", []) or payload.get("conversation", [])
        temperature = payload.get("temperature")

        throttle_delay_ms = int(config.get("LLM_THROTTLE_DELAY", 0))
        if throttle_delay_ms:
            sleep(throttle_delay_ms / 1000.0)

        # Delegate to provider client
        try:
            response = client.chat(
                messages=conversation,
                temperature=temperature,
            )
            print(f"[LLM API] Provider '{provider}' returned response keys: {list(response.keys()) if isinstance(response, dict) else type(response)}")
            return jsonify(response)
        except Exception as exc:  # Provider errors surface in a uniform shape
            status_code = 500
            message = str(exc)
            if isinstance(exc, requests.exceptions.HTTPError) and exc.response is not None:
                status_code = exc.response.status_code or 500
                try:
                    message = exc.response.json().get("error", {}).get("message", message)
                except Exception:
                    message = exc.response.text or message
            print(f"[LLM API] Error ({status_code}): {message}")
            return jsonify({"error": {"message": message}}), status_code

    return app

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("LLM_API_PORT", "5001"))
    app.run(host="0.0.0.0", port=port)
