import json
from typing import Dict, Tuple, List
from .config import get_config
from .read import read_addresses
from langchain.tools import tool

from api.utils.console import print_to_console

_config = get_config()
_RAMDISK_DIR = _config['RAMDISK_DIR']
_RAM_CONTENTS_PATH = _RAMDISK_DIR + 'ram_contents.json'

def _load_ram_contents() -> Dict[str, str]:
    with open(_RAM_CONTENTS_PATH, 'r') as f:
        return json.load(f)

# Addresses for the four character names (4 letters each)
NAME_ADDRESSES: List[str] = [
    "0x006102", "0x006103", "0x006104", "0x006105",
    "0x006142", "0x006143", "0x006144", "0x006145",
    "0x006182", "0x006183", "0x006184", "0x006185",
    "0x0061C2", "0x0061C3", "0x0061C4", "0x0061C5"
]

def get_names() -> Tuple[Dict[str, str], int]:
    """
    Return the four character names by reading the NAME_ADDRESSES.

    Returns (result, status) where result is a dict:
      {"character_1": "Name1", "character_2": "Name2", ...}
    """
    # Use read_addresses to perform validation and lookups
    try:
        result, status = read_addresses(NAME_ADDRESSES)
    except Exception as e:
        return (f"Error calling read_addresses: {e}", 500)

    if status != 200:
        return (result, status)

    addresses_map = result.get('addresses') if isinstance(result, dict) else None
    if not addresses_map or not isinstance(addresses_map, dict):
        return ("Unexpected result from read_addresses", 500)

    # Build names by concatenating each group of 4 addresses
    try:
        name_1 = ''.join([addresses_map.get(addr, '') for addr in NAME_ADDRESSES[0:4]])
        name_2 = ''.join([addresses_map.get(addr, '') for addr in NAME_ADDRESSES[4:8]])
        name_3 = ''.join([addresses_map.get(addr, '') for addr in NAME_ADDRESSES[8:12]])
        name_4 = ''.join([addresses_map.get(addr, '') for addr in NAME_ADDRESSES[12:16]])
    except Exception as e:
        return (f"Error building names: {e}", 500)

    return ({
        "character_1": name_1,
        "character_2": name_2,
        "character_3": name_3,
        "character_4": name_4
    }, 200)


__all__ = ["NAME_ADDRESSES", "get_names"]


@tool
def get_names_tool(arg_str: str) -> str:
    """
    LangChain tool wrapper around `get_names` that accepts an optional JSON
    string and returns a JSON string result.

    Input examples:
      '{}'
      'null'

    Output example: '{"character_1":"ABCD","character_2":"EFGH",...}'
    """
    print_to_console()
    print_to_console('Calling get_names tool:', color='yellow')
    print_to_console('arg_str = ' + str(arg_str))

    # We don't require any specific input; just call get_names
    try:
        result, status = get_names()
    except Exception as e:
        print_to_console('error = ' + str(e), 'red')
        return '{"error": "' + str(e) + '"}'

    if status != 200:
        print_to_console('error = ' + str(result), 'red')
        return '{"error": "' + str(result) + '"}'

    try:
        print_to_console('result = ' + json.dumps(result))
        return json.dumps(result)
    except Exception as e:
        print_to_console('error = ' + str(e), 'red')
        return '{"error": "' + str(e) + '"}'
