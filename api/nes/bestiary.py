import json
from .config import get_config
from typing import Dict, Any, List, Tuple

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
