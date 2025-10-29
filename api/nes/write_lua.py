from .config import get_config

config = get_config()
FILENAME = config['RAMDISK_DIR'] + "execute.lua"

def write_lua_script(lua_script: str):
    """
    Write a raw Lua script string to the RAM disk execute.lua file.
    Returns tuple (message, status_code).
    """
    if not lua_script:
        return "Missing file content", 400

    try:
        with open(FILENAME, 'w') as f:
            f.write(lua_script)
        return f"'{FILENAME}' written successfully", 200
    except Exception as e:
        return f"Error writing file: {e}", 500
