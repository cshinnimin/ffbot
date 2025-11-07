from flask import Flask, request, jsonify
from flask_cors import CORS
from time import sleep
import os
import requests
from .config import get_config
from .llm_client import create_client
from api.utils.console import print_to_console

def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app)

    config = get_config()

    # Instantiate LLM client via the factory in the llm_client package
    provider = config["LLM_PROVIDER"].lower()
    client = create_client(config)

    print_to_console(f"LLM provider '{provider}' initialized with model '{config.get('LLM_MODEL')}'", 'yellow')

    @app.route("/llm/get-response", methods=["POST", "OPTIONS"])
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
            print_to_console(f"LLM provider '{provider}' returned response keys: {list(response.keys()) if isinstance(response, dict) else type(response)}", 'yellow')
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
            print_to_console(f"LLM provider error ({status_code}): {message}", 'red')
            return jsonify({"error": {"message": message}}), status_code

    return app

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("LLM_API_PORT", "5001"))
    app.run(host="0.0.0.0", port=port)
