from flask import Flask, request
from flask_cors import CORS
import os
from .config import get_config
from .write_lua import write_lua_script
from .write import write_addresses

def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app)

    config = get_config()

    @app.route('/nes/write-lua', methods=['POST', 'OPTIONS'])
    def _write_lua_route():
        if request.method == 'OPTIONS':
            return ('', 200)
        
        payload = request.get_json(silent=True) or {}
        lua_script = payload.get('lua_script')
        message, status = write_lua_script(lua_script)
        
        return (message, status)

    @app.route('/nes/write', methods=['POST', 'OPTIONS'])
    def _write_route():
        if request.method == 'OPTIONS':
            return ('', 200)
        
        payload = request.get_json(silent=True) or {}
        addresses = payload.get('addresses')
        message, status = write_addresses(addresses)

        return (message, status)

    return app

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('NES_API_PORT', str(get_config().get('NES_API_PORT', 5000))))
    app.run(host='0.0.0.0', port=port)
