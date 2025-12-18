from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from .config import get_config
from .write_lua import write_lua_script
from .write import write_addresses
from .read import read_addresses
from .bestiary import get_monsters_by_location
from .bestiary import get_locations_by_monster
from .names import get_names

def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app)

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

    @app.route('/nes/read', methods=['POST', 'OPTIONS'])
    def _read_route():
        if request.method == 'OPTIONS':
            return ('', 200)
        
        payload = request.get_json(silent=True) or {}
        addresses = payload.get('addresses')
        result, status = read_addresses(addresses)

        if status != 200:
            return (jsonify({"error": result}), status)
        
        return (jsonify(result), 200)

    @app.route('/nes/bestiary/get-monsters-by-location', methods=['POST', 'OPTIONS'])
    def _get_monsters_by_location_route():
        if request.method == 'OPTIONS':
            return ('', 200)

        payload = request.get_json(silent=True) or {}
        location = payload.get('location')
        result, status = get_monsters_by_location(location)

        if status != 200:
            return (jsonify({"error": result}), status)

        return (jsonify(result), 200)

    @app.route('/nes/bestiary/get-locations-by-monster', methods=['POST', 'OPTIONS'])
    def _get_locations_by_monster_route():
        if request.method == 'OPTIONS':
            return ('', 200)

        payload = request.get_json(silent=True) or {}
        monsters = payload.get('monsters')
        result, status = get_locations_by_monster(monsters)

        if status != 200:
            return (jsonify({"error": result}), status)

        return (jsonify(result), 200)

    @app.route('/nes/names/get', methods=['POST', 'OPTIONS'])
    def _get_names_route():
        if request.method == 'OPTIONS':
            return ('', 200)

        # No payload required; simply return the four character names
        result, status = get_names()

        if status != 200:
            return (jsonify({"error": result}), status)

        return (jsonify(result), 200)

    return app

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('NES_API_PORT', str(get_config().get('NES_API_PORT', 5000))))
    app.run(host='0.0.0.0', port=port)
