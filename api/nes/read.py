from .config import get_config
import json
from typing import Tuple, Dict, Any, List

"""
Read endpoint implementation.

Exposes a function `read_addresses(addresses)` which accepts a parsed list
of address strings (e.g., ["0x006BE4", "0x006BE5"]) and returns a tuple
(result, status). On success, result is a dict of the form
{"addresses": {addr: value, ...}} and status is 200. On failure, result
is an error message string and status is an HTTP error code.
"""

_config = get_config()
_RAMDISK_DIR = _config['RAMDISK_DIR']
_RAM_CATALOG_PATH = _RAMDISK_DIR + 'ram_catalog.json'
_RAM_CONTENTS_PATH = _RAMDISK_DIR + 'ram_contents.json'

def _load_ram_catalog() -> Dict[str, Any]:
    """
    Load and return the entries_map built from ram_catalog.json.

    entries_map: address -> either { description, weight } or { description, lookup }
    This function caches the parsed entries for the lifetime of the process.
    """
    # Cache parsed entries for lifetime of process — the catalog is static.
    global _RAM_CATALOG_ENTRIES_CACHE
    try:
        if _RAM_CATALOG_ENTRIES_CACHE is not None:
            return _RAM_CATALOG_ENTRIES_CACHE
    except NameError:
        # first-time load
        _RAM_CATALOG_ENTRIES_CACHE = None

    with open(_RAM_CATALOG_PATH, 'r') as f:
        ram_catalog = json.load(f)

    lookups: Dict[str, Any] = {}
    for item in ram_catalog.get('lookups', []) or []:
        # each lookup item should have `key`, `default`, and `map`
        lookups[item['key']] = {
            'default': item.get('default'),
            'map': item.get('map', {})
        }

    entries: Dict[str, Any] = {}
    for catalog_entry in ram_catalog.get('catalog', []) or []:
        if catalog_entry.get('type') == 'number':
            entries[catalog_entry['address']] = {
                'description': catalog_entry.get('description', ''),
                'weight': catalog_entry.get('weight')
            }
        elif catalog_entry.get('type') == 'lookup':
            lookup_key = catalog_entry.get('lookup')
            lookup = lookups.get(lookup_key)
            entries[catalog_entry['address']] = {
                'description': catalog_entry.get('description', ''),
                'lookup': lookup
            }
        else:
            # keep empty/unknown types as-is (will be rejected later)
            entries[catalog_entry['address']] = {
                'description': catalog_entry.get('description', ''),
                'type': catalog_entry.get('type', '')
            }

    _RAM_CATALOG_ENTRIES_CACHE = entries
    return _RAM_CATALOG_ENTRIES_CACHE


def _load_ram_contents() -> Dict[str, str]:
    with open(_RAM_CONTENTS_PATH, 'r') as f:
        return json.load(f)

"""
 Private function used to confirm whether there is really an Imp in a given enemy slot.
 Since Imps enemy code is 00, and ALL enemy data values are set to 00 in slots with no
 enemy, additonal logic is required to validate that an Imp really exists in the slot.
"""
def _confirm_imp(address: str, ram_contents: Dict[str, str]) -> str:
    # map whose key is the memory address of an enemy type, and whose value is the
    # memory address of the corresponding enemy "exists?" flag:
    EXISTS_BY_TYPE_ADDRESS_MAP = {
        "0x006BE4": "0x006BDF",
        "0x006BF8": "0x006BF3",
        "0x006C0C": "0x006C07",
        "0x006C20": "0x006C1B",
        "0x006C34": "0x006C2F",
        "0x006C48": "0x006C43",
        "0x006C5C": "0x006C57",
        "0x006C70": "0x006C6B",
        "0x006C84": "0x006C7F"
    }

    exists_addr = EXISTS_BY_TYPE_ADDRESS_MAP.get(address)
    if not exists_addr:
        return "Imp"
    if ram_contents.get(exists_addr) == "0x00":
        return ""
    return "Imp"


def read_addresses(addresses: List[str]) -> Tuple[Dict[str, Any], int]:
    """
    Read RAM values for the given addresses list and translate them into values meaningful
    to a human or an LLM.
    
    Returns (result, status). On success result is {"addresses": {...}}.
    """

    # Validate input type
    if not isinstance(addresses, list):
        return ("addresses must be a list of address strings", 400)

    # Load ram_catalog.json and RAM contents
    try:
        entries = _load_ram_catalog()
    except FileNotFoundError:
        return (f"ram_catalog.json not found at {_RAM_CATALOG_PATH}", 500)
    except Exception as e:
        return (f"Error loading ram_catalog.json: {e}", 500)

    try:
        ram_contents = _load_ram_contents()
    except FileNotFoundError:
        return (f"ram_contents.json not found at {_RAM_CONTENTS_PATH}", 500)
    except Exception as e:
        return (f"Error loading ram_contents.json: {e}", 500)

    # Check for missing addresses in catalog
    missing = [a for a in addresses if a not in entries]
    if missing:
        return (f"Requested RAM addresses not found in ram_catalog.json: {missing}", 400)

    # Build response map
    values = {}
    try:
        for address in addresses:
            entry = entries[address]
            
            if 'lookup' in entry and entry.get('lookup') is not None:
                # entry is a "Lookup entry"
                # Lookup entries have their raw value translated using the lookup
                # table referenced in ram_contents.json for the particular address

                lookup = entry['lookup']
                raw = ram_contents.get(address)
                mapped = lookup['map'].get(raw) if lookup and 'map' in lookup else None
                if mapped is not None:
                    values[address] = mapped
                else:
                    values[address] = lookup.get('default') if lookup else None

                if values[address] == "Imp":
                    values[address] = _confirm_imp(address, ram_contents)

            elif 'weight' in entry:
                # entry is a "Number entry"
                # Number entries have their raw value in memory multiplied by the weight
                # specified in ram_contents.json for the particular address

                raw = ram_contents.get(address)
                # parse hex (e.g., '0x05')
                try:
                    raw_val = int(raw, 16) if isinstance(raw, str) else int(raw)
                except Exception:
                    return ("Game memory not in expected format. Perhaps a RAM address I have been trained on is not available for lookup.", 500)
                
                weight = int(entry['weight']) if entry.get('weight') is not None else 1
                values[address] = str(raw_val * weight)
            else:
                return ("RAM Catalog entry has unexpected format.", 500)
    except Exception as e:
        return (f"Game memory not in expected format: {e}", 500)

    return ({"addresses": values}, 200)

__all__ = ["read_addresses"]
