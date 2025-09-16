import os
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes and allow all origins

FILENAME = os.environ['RAMDISK_DIR'] + "execute.lua"

@app.route('/write_ram', methods=['POST'])
def write_ram():
    post = request.get_json()

    if not post or 'lua_script' not in post:
        return "Missing file content", 400

    lua_script = post['lua_script']

    try:
        with open(FILENAME, 'w') as f:
            f.write(lua_script)
        return f"'{FILENAME}' written successfully", 200
    except Exception as e:
        return f"Error writing file: {e}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)