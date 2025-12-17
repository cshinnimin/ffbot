import json
from typing import Dict, Any, Tuple, List
from .config import get_config
from .read import read_addresses
from .write import write_addresses
from langchain.tools import tool

from api.utils.console import print_to_console

_config = get_config()
_RAMDISK_DIR = _config['RAMDISK_DIR']
_RAM_CONTENTS_PATH = _RAMDISK_DIR + 'ram_contents.json'

def _load_ram_contents() -> Dict[str, str]:
    with open(_RAM_CONTENTS_PATH, 'r') as f:
        return json.load(f)

# STAT_ADDRESSES: 4 slots, each with a list of addresses (strings)
STAT_ADDRESSES: List[List[str]] = [
    [
        "0x006100", "0x006101", "0x006102", "0x006103", "0x006104", "0x006105",
        "0x006106", "0x006107", "0x006108", "0x006109", "0x00610A", "0x00610B",
        "0x00610C", "0x00610D", "0x00610E", "0x00610F", "0x006110", "0x006111",
        "0x006112", "0x006113", "0x006114", "0x006115", "0x006116", "0x006117",
        "0x006118", "0x006119", "0x00611A", "0x00611B", "0x00611C", "0x00611D",
        "0x00611E", "0x00611F", "0x006120", "0x006121", "0x006122", "0x006123",
        "0x006124", "0x006125", "0x006126", "0x006127", "0x006128", "0x006129",
        "0x00612A", "0x00612B", "0x00612C", "0x00612D", "0x00612E", "0x00612F",
        "0x006130", "0x006131", "0x006132", "0x006133", "0x006134", "0x006135",
        "0x006136", "0x006137", "0x006138", "0x006139", "0x00613A", "0x00613B",
        "0x00613C", "0x00613D", "0x00613E", "0x00613F"
    ],
    [
        "0x006140", "0x006141", "0x006142", "0x006143", "0x006144", "0x006145",
        "0x006146", "0x006147", "0x006148", "0x006149", "0x00614A", "0x00614B",
        "0x00614C", "0x00614D", "0x00614E", "0x00614F", "0x006150", "0x006151",
        "0x006152", "0x006153", "0x006154", "0x006155", "0x006156", "0x006157",
        "0x006158", "0x006159", "0x00615A", "0x00615B", "0x00615C", "0x00615D",
        "0x00615E", "0x00615F", "0x006160", "0x006161", "0x006162", "0x006163",
        "0x006164", "0x006165", "0x006166", "0x006167", "0x006168", "0x006169",
        "0x00616A", "0x00616B", "0x00616C", "0x00616D", "0x00616E", "0x00616F",
        "0x006170", "0x006171", "0x006172", "0x006173", "0x006174", "0x006175",
        "0x006176", "0x006177", "0x006178", "0x006179", "0x00617A", "0x00617B",
        "0x00617C", "0x00617D", "0x00617E", "0x00617F"
    ],
    [
        "0x006180", "0x006181", "0x006182", "0x006183", "0x006184", "0x006185",
        "0x006186", "0x006187", "0x006188", "0x006189", "0x00618A", "0x00618B",
        "0x00618C", "0x00618D", "0x00618E", "0x00618F", "0x006190", "0x006191",
        "0x006192", "0x006193", "0x006194", "0x006195", "0x006196", "0x006197",
        "0x006198", "0x006199", "0x00619A", "0x00619B", "0x00619C", "0x00619D",
        "0x00619E", "0x00619F", "0x0061A0", "0x0061A1", "0x0061A2", "0x0061A3",
        "0x0061A4", "0x0061A5", "0x0061A6", "0x0061A7", "0x0061A8", "0x0061A9",
        "0x0061AA", "0x0061AB", "0x0061AC", "0x0061AD", "0x0061AE", "0x0061AF",
        "0x0061B0", "0x0061B1", "0x0061B2", "0x0061B3", "0x0061B4", "0x0061B5",
        "0x0061B6", "0x0061B7", "0x0061B8", "0x0061B9", "0x0061BA", "0x0061BB",
        "0x0061BC", "0x0061BD", "0x0061BE", "0x0061BF"
    ],
    [
        "0x0061C0", "0x0061C1", "0x0061C2", "0x0061C3", "0x0061C4", "0x0061C5",
        "0x0061C6", "0x0061C7", "0x0061C8", "0x0061C9", "0x0061CA", "0x0061CB",
        "0x0061CC", "0x0061CD", "0x0061CE", "0x0061CF", "0x0061D0", "0x0061D1",
        "0x0061D2", "0x0061D3", "0x0061D4", "0x0061D5", "0x0061D6", "0x0061D7",
        "0x0061D8", "0x0061D9", "0x0061DA", "0x0061DB", "0x0061DC", "0x0061DD",
        "0x0061DE", "0x0061DF", "0x0061E0", "0x0061E1", "0x0061E2", "0x0061E3",
        "0x0061E4", "0x0061E5", "0x0061E6", "0x0061E7", "0x0061E8", "0x0061E9",
        "0x0061EA", "0x0061EB", "0x0061EC", "0x0061ED", "0x0061EE", "0x0061EF",
        "0x0061F0", "0x0061F1", "0x0061F2", "0x0061F3", "0x0061F4", "0x0061F5",
        "0x0061F6", "0x0061F7", "0x0061F8", "0x0061F9", "0x0061FA", "0x0061FB",
        "0x0061FC", "0x0061FD", "0x0061FE", "0x0061FF"
    ]
]

def order_party(slot1: int, slot2: int, slot3: int, slot4: int) -> Tuple[Any, int]:
    """
    Reorder the party by copying stat blocks from source slots to destination slots.

    Each argument indicates which previous slot should be moved into that destination.
    For example, (2,4,3,1) means:
      - what was in slot 2 -> slot 1
      - what was in slot 4 -> slot 2
      - what was in slot 3 -> slot 3
      - what was in slot 1 -> slot 4

    Returns (result, status) where result is a message or error.
    """
    # Validate inputs
    slots = [slot1, slot2, slot3, slot4]
    if not all(isinstance(s, int) for s in slots):
        return ("All slots must be integers", 400)
    if set(slots) != {1, 2, 3, 4}:
        return ("Slots must be a permutation of 1..4", 400)

    try:
        ram_contents = _load_ram_contents()
    except FileNotFoundError:
        return ("ram_contents.json not found", 500)
    except Exception as e:
        return (f"Error loading ram_contents.json: {e}", 500)

    # Build write payload: for each destination slot index, copy values from the
    # corresponding source slot's addresses into the destination addresses.
    write_payload: Dict[str, str] = {}
    try:
        for dest_idx in range(4):
            src_idx = slots[dest_idx] - 1
            dest_addrs = STAT_ADDRESSES[dest_idx]
            src_addrs = STAT_ADDRESSES[src_idx]

            if len(dest_addrs) != len(src_addrs):
                return ("Internal address length mismatch", 500)

            for i, dest_addr in enumerate(dest_addrs):
                src_addr = src_addrs[i]
                val = ram_contents.get(src_addr)
                if val is None:
                    return (f"Missing expected RAM address in ram_contents: {src_addr}", 500)
                write_payload[dest_addr] = val
    except Exception as e:
        return (f"Error preparing write payload: {e}", 500)

    # Call write_addresses to perform the memory writes
    try:
        result, status = write_addresses(write_payload)
    except Exception as e:
        return (f"Error calling write_addresses: {e}", 500)

    return (result, status)


__all__ = ["STAT_ADDRESSES", "order_party"]

@tool
def order_party_tool(arg_str: str) -> str:
    """
    LangChain tool wrapper around `order_party` that accepts a JSON array like
    "[2,4,3,1]" or a JSON object {"slot1":2,...} and returns a JSON string result.
    """
    print_to_console()
    print_to_console('Calling order_party tool:', color='yellow')
    print_to_console('arg_str = ' + str(arg_str))

    if arg_str is None:
        return '{"error": "Missing arg_str"}'

    formatted = str(arg_str).strip()
    # unwrap backticks/quotes if present
    if (formatted.startswith('`') and formatted.endswith('`')) or (formatted.startswith('```') and formatted.endswith('```')):
        formatted = formatted.strip('`').strip()
    if (formatted.startswith('"') and formatted.endswith('"')) or (formatted.startswith("'") and formatted.endswith("'")):
        formatted = formatted[1:-1].strip()

    payload = None
    try:
        payload = json.loads(formatted)
    except Exception:
        # Try single-quote -> double-quote
        try:
            payload = json.loads(formatted.replace("'", '"'))
        except Exception:
            try:
                import ast
                payload = ast.literal_eval(formatted)
            except Exception as e:
                return '{"error": "failed to parse arg_str: ' + str(e).replace('"','') + '"}'

    # Accept either a list [2,4,3,1] or object {"slot1":2,...}
    try:
        if isinstance(payload, list):
            if len(payload) != 4:
                return '{"error": "expected list of four slot integers"}'
            s1, s2, s3, s4 = payload
        elif isinstance(payload, dict):
            s1 = int(payload.get('slot1'))
            s2 = int(payload.get('slot2'))
            s3 = int(payload.get('slot3'))
            s4 = int(payload.get('slot4'))
        else:
            return '{"error": "unexpected arg format"}'
    except Exception as e:
        return '{"error": "invalid slot values: ' + str(e).replace('"','') + '"}'

    result, status = order_party(s1, s2, s3, s4)
    if status != 200:
        print_to_console('error = ' + str(result), 'red')
        return '{"error": "' + str(result).replace('"','') + '"}'

    try:
        print_to_console('result = ' + json.dumps(result))
        return json.dumps({"message": result})
    except Exception as e:
        print_to_console('error = ' + str(e), 'red')
        return '{"error": "' + str(e).replace('"','') + '"}'
