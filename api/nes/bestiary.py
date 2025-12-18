import json
from .config import get_config
from typing import Dict, Any, List, Tuple
from langchain.tools import tool

from api.utils.console import print_to_console

"""
Bestiary loader.

Provides `_load_bestiary()` which returns a tuple `(bestiary, reverse_bestiary)`:
- `bestiary`: Dict[str, List[str]] mapping location -> list of monster names
- `reverse_bestiary`: Dict[str, List[str]] mapping normalized monster name -> list of locations

The function caches the parsed bestiary for the lifetime of the process.
"""

_config = get_config()
_RAMDISK_DIR = _config['RAMDISK_DIR']
_BESTIARY_PATH = _RAMDISK_DIR + 'bestiary.json'

def _load_bestiary() -> Tuple[Dict[str, List[str]], Dict[str, List[str]]]:
    """
    Load and return the bestiary and reverse bestiary maps built from bestiary.json.

    The bestiary file is expected to be a JSON object whose keys are location
    strings and whose values are arrays of monster names. Example:
    {
      "(Some Location)": ["Imp", "Goblin"],
      "(Another Place)": ["Cerebus"]
    }

    Returns (bestiary, reverse_bestiary)
    """
    # Cache parsed entries for lifetime of process — the bestiary is static.
    global _BESTIARY_CACHE, _REVERSE_BESTIARY_CACHE
    try:
        if _BESTIARY_CACHE is not None and _REVERSE_BESTIARY_CACHE is not None:
            return (_BESTIARY_CACHE, _REVERSE_BESTIARY_CACHE)
    except NameError:
        _BESTIARY_CACHE = None
        _REVERSE_BESTIARY_CACHE = None

    with open(_BESTIARY_PATH, 'r') as f:
        bestiary_data = json.load(f)

    bestiary: Dict[str, List[str]] = bestiary_data or {}
    reverse_bestiary: Dict[str, List[str]] = {}

    def normalize(name: str) -> str:
        return ''.join([c for c in name.lower() if c.isalnum()])

    for loc, monsters in bestiary.items():
        # ensure monsters is a list
        if not isinstance(monsters, list):
            continue
        for monster in monsters:
            key = normalize(monster)
            if key not in reverse_bestiary:
                reverse_bestiary[key] = []
            reverse_bestiary[key].append(loc)

    _BESTIARY_CACHE = bestiary
    _REVERSE_BESTIARY_CACHE = reverse_bestiary
    return (_BESTIARY_CACHE, _REVERSE_BESTIARY_CACHE)


def get_monsters_by_location(location: str) -> Tuple[Dict[str, List[str]], int]:
    """
    Return the monsters list for the given `location` key from the cached bestiary.

    Ensures the bestiary cache is loaded by calling `_load_bestiary()` first.

    Returns a tuple `(result, status)` where `result` is a dict of the form
    `{"monsters": [...]}` on success, or an error message string on failure.
    """
    if not isinstance(location, str):
        return ("location must be a string", 400)

    try:
        bestiary, _ = _load_bestiary()
    except FileNotFoundError:
        return (f"bestiary.json not found at {_BESTIARY_PATH}", 500)
    except Exception as e:
        return (f"Error loading bestiary.json: {e}", 500)

    monsters = bestiary.get(location) or ["no monsters here"]
    return ({"monsters": monsters}, 200)


__all__ = ["_load_bestiary", "get_monsters_by_location"]


def get_locations_by_monster(monsters: List[str]) -> Tuple[Dict[str, Dict[str, List[str]]], int]:
    """
    Given a list of monster names, return a mapping from each (possibly-singularized)
    monster string to a list of locations where that monster appears.

    This mirrors `requestLocationsByMonster` in the frontend hook: it will strip a
    trailing 's' from monster names (except 'cerebus' and 'chaos') before lookup.

    Returns (result, status) where `result` is of the form {"locations": {monster: [locs]}}
    on success, or an error message string and HTTP status on failure.
    """
    if not isinstance(monsters, list):
        return ("monsters must be a list", 400)

    try:
        _, reverse_bestiary = _load_bestiary()
    except FileNotFoundError:
        return (f"bestiary.json not found at {_BESTIARY_PATH}", 500)
    except Exception as e:
        return (f"Error loading bestiary.json: {e}", 500)

    def singularize(name: str) -> str:
        low = name.lower()
        if low not in ("cerebus", "chaos") and low.endswith('s'):
            return name[:-1]
        return name

    def normalize(name: str) -> str:
        return ''.join([c for c in name.lower() if c.isalnum()])

    locations_obj: Dict[str, List[str]] = {}
    for m in monsters:
        if not isinstance(m, str):
            locations_obj[str(m)] = ["monster not found"]
            continue

        singular = singularize(m)
        key = normalize(singular)
        locations = reverse_bestiary.get(key) or ["monster not found"]
        locations_obj[singular] = locations

    return ({"locations": locations_obj}, 200)


__all__.append("get_locations_by_monster")


# Provide LangChain tool wrappers while keeping the core functions plain for Flask/other usage.
@tool
def get_monsters_by_location_tool(arg_str: str) -> str:
    """
    LangChain tool wrapper around `get_monsters_by_location` that accepts a JSON string
    (as provided by the LLM) and returns a JSON string result (expected by the LLM).

    Input examples:
      '"(Some Location)"'
      '{"location": "(Some Location)"}'

    Output example: '{"monsters": ["Imp", "Goblin"]}'
    """
    print_to_console()
    print_to_console('Calling get_monsters_by_location tool:', color='yellow')
    print_to_console('arg_str = ' + arg_str)

    # Parse location from the LLM-provided JSON string
    try:
        parsed = json.loads(arg_str)
        if isinstance(parsed, dict) and 'location' in parsed:
            location = parsed['location']
        else:
            # assume the parsed value itself is the location string
            location = parsed
    except Exception as e:
        print_to_console(f'error = {e}', 'red')
        return '{"error": "Failed to parse tool input: ' + str(e) + '"}'

    result, status = get_monsters_by_location(location)
    if status != 200:
        print_to_console('error = ' + str(result), 'red')
        return '{"error": "' + str(result) + '"}'

    try:
        print_to_console('result = ' + json.dumps(result))
        return json.dumps(result)
    except Exception as e:
        print_to_console('error = ' + str(e), 'red')
        return '{"error": "' + str(e) + '"}'


@tool
def get_locations_by_monster_tool(arg_str: str) -> str:
    """
    LangChain tool wrapper around `get_locations_by_monster` that accepts a JSON string
    (as provided by the LLM) and returns a JSON string result (expected by the LLM).

    Input examples:
      '["Goblin","Imps"]'
      '{"monsters": ["Goblin","Imps"]}'

    Output example: '{"locations": {"Goblin": ["(Loc1)"], "Imp": ["(Loc2)"]}}'
    """
    print_to_console()
    print_to_console('Calling get_locations_by_monster tool:', color='yellow')
    print_to_console('arg_str = ' + arg_str)

    try:
        parsed = json.loads(arg_str)
        if isinstance(parsed, dict) and 'monsters' in parsed:
            monsters = parsed['monsters']
        else:
            monsters = parsed
    except Exception as e:
        print_to_console(f'error = {e}', 'red')
        return '{"error": "Failed to parse tool input: ' + str(e) + '"}'

    result, status = get_locations_by_monster(monsters)
    if status != 200:
        print_to_console('error = ' + str(result), 'red')
        return '{"error": "' + str(result) + '"}'

    try:
        print_to_console('result = ' + json.dumps(result))
        return json.dumps(result)
    except Exception as e:
        print_to_console('error = ' + str(e), 'red')
        return '{"error": "' + str(e) + '"}'

