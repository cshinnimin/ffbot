from typing import Optional
import os
import sys

# Centralised flag controlling whether colour output is enabled. This is the
# single authoritative source of truth for colour printing across the project.
_USE_COLOUR = sys.stdout.isatty() and not os.environ.get('NO_COLOR')

# Mapping of friendly colour names to ANSI escape code sequences. Use the
# same bold yellow code used elsewhere for 'yellow' to preserve prior look.
_COLOR_CODES = {
    'black': '0;30',
    'red': '0;31',
    'green': '0;32',
    'yellow': '1;33',
    'blue': '0;34',
    'magenta': '0;35',
    'cyan': '0;36',
    'white': '0;37',
}

def print_to_console(text: Optional[str] = '', color: Optional[str] = None) -> None:
    """
    Print text to the console. `text` may be omitted; it defaults to an
    empty string. If `color` is provided and colour output is enabled via
    the internal `_USE_COLOUR` flag, the text will be wrapped in the
    corresponding ANSI colour escape sequences. Otherwise the text is printed
    plainly.

    This function is the single place that defines and uses `_USE_COLOUR`.
    """
    # Ensure we have a string to print
    if text is None:
        text = ''

    if color and _USE_COLOUR:
        code = _COLOR_CODES.get(color, '')
        if code:
            print(f"\x1b[{code}m{text}\x1b[0m")
            return

    # Default: plain print
    print(text)
